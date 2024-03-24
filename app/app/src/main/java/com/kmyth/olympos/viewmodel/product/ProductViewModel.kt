package com.kmyth.olympos.viewmodel.product

import androidx.lifecycle.LiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.asLiveData
import androidx.lifecycle.viewModelScope
import com.kmyth.olympos.model.product.GroupListRequestModel
import com.kmyth.olympos.model.product.GroupListResponseModel
import com.kmyth.olympos.model.product.GroupModel
import com.kmyth.olympos.network.RetrofitClient
import com.kmyth.olympos.network.ServerCallInterface
import com.kmyth.olympos.viewmodel.login.UserPreferencesRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import retrofit2.Call
import retrofit2.Response
import retrofit2.Retrofit
import timber.log.Timber

class ProductViewModel(
    private val repository: ProductRepository,
    private val userPreferencesRepository: UserPreferencesRepository
): ViewModel() {

    init {
        viewModelScope.launch(Dispatchers.Default) {
            userPreferencesRepository.fetchInitialPreferences()
        }
    }

    private val _groupListState = MutableStateFlow<List<GroupModel>>(emptyList())
    val groupListState: StateFlow<List<GroupModel>> = _groupListState.asStateFlow()

    private val storeIdFlow = userPreferencesRepository.storeIdFlow
    private val storeIdLivaData: LiveData<Int> = storeIdFlow.asLiveData()

    fun getGroupList(SSAID: String, ) {
        viewModelScope.launch(Dispatchers.Default) {
            storeIdFlow.collectLatest { storeId ->
                val model = GroupListRequestModel(SSAID, storeId)
                repository.getGroupList(model, _groupListState)
            }
        }
    }
}

class ProductViewModelFactory(
    private val repository: ProductRepository,
    private val userPreferencesRepository: UserPreferencesRepository
    ): ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(ProductViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return ProductViewModel(repository, userPreferencesRepository) as T
        }

        throw IllegalArgumentException("Unknown ViewModel class :: ${modelClass::class.java.simpleName}")
    }
}

interface ProductRepository {
    fun getGroupList(model: GroupListRequestModel, stateFlow: MutableStateFlow<List<GroupModel>>)
}

class ProductRepositoryImpl: ProductRepository {
    override fun getGroupList(model: GroupListRequestModel, stateFlow: MutableStateFlow<List<GroupModel>>) {
        val service: Retrofit? = RetrofitClient.getClient()
        service?.create(ServerCallInterface::class.java)
            ?.getGroupList(model.toMap())
            ?.enqueue(object: retrofit2.Callback<GroupListResponseModel> {
                override fun onResponse(
                    call: Call<GroupListResponseModel>,
                    response: Response<GroupListResponseModel>
                ) {
                    if (response.isSuccessful) {
                        val body = response.body()
                        if (body != null) {
                            if (body.result == "Success") {
                                stateFlow.value = body.groups
                            } else {
                                // TODO : fail 처리
                                Timber.d("getGroupList body.result = ${body.result}, body.code = ${body.code}")
                            }
                        } else {
                            // TODO : fail 처리
                            Timber.d("getGroupList Response Error")
                        }
                    } else {
                        // TODO : fail 처리
                        Timber.d("getGroupList Response Failed")
                    }
                }

                override fun onFailure(call: Call<GroupListResponseModel>, t: Throwable) {
                    // TODO : fail 처리
                    Timber.d("getGroupList onFailure - ${t.message}")
                }
            })
    }
}