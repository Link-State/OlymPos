package com.kmyth.olympos.viewmodel.product

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.kmyth.olympos.model.product.GroupListRequestModel
import com.kmyth.olympos.model.product.GroupListResponseModel
import com.kmyth.olympos.model.product.GroupModel
import com.kmyth.olympos.model.product.OptionListRequestModel
import com.kmyth.olympos.model.product.OptionListResponseModel
import com.kmyth.olympos.model.product.OptionModel
import com.kmyth.olympos.model.product.ProductListRequestModel
import com.kmyth.olympos.model.product.ProductListResponseModel
import com.kmyth.olympos.model.product.ProductModel
import com.kmyth.olympos.network.RetrofitClient
import com.kmyth.olympos.network.ServerCallInterface
import com.kmyth.olympos.viewmodel.login.UserPreferencesRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.firstOrNull
import kotlinx.coroutines.launch
import retrofit2.Call
import retrofit2.Response
import retrofit2.Retrofit
import timber.log.Timber

class ProductViewModel(
    private val repository: ProductRepository,
    private val userPreferencesRepository: UserPreferencesRepository
): ViewModel() {

    private lateinit var SSAID: String
    private var storeId: Int = -1

    private val storeIdFlow = userPreferencesRepository.storeIdFlow

    init {
        viewModelScope.launch(Dispatchers.Default) {
            userPreferencesRepository.fetchInitialPreferences()
            storeId = storeIdFlow.firstOrNull() ?: -1
        }
    }

    private val _groupListState = MutableStateFlow<List<GroupModel>>(emptyList())
    val groupListState: StateFlow<List<GroupModel>> = _groupListState.asStateFlow()

    private val _productListState = MutableStateFlow<List<ProductModel>>(emptyList())
    val productListState: StateFlow<List<ProductModel>> = _productListState.asStateFlow()

    private val _optionListState = MutableStateFlow<List<OptionModel>>(emptyList())
    val optionListState: StateFlow<List<OptionModel>> = _optionListState.asStateFlow()

    fun updateProduct(SSAID: String) {
        Timber.d("updateProduct")
        this.SSAID = SSAID

        getGroupList()
        getProductList()
        getOptionList()
    }

    private fun getGroupList() {
        val model = GroupListRequestModel(SSAID, storeId)
        repository.getGroupList(model, _groupListState)
    }

    private fun getProductList() {
        val model = ProductListRequestModel(SSAID, storeId)
        repository.getProductList(model, _productListState)
    }

    private fun getOptionList() {
        val model = OptionListRequestModel(SSAID, storeId)
        repository.getOptionList(model, _optionListState)
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
    fun getProductList(model: ProductListRequestModel, stateFlow: MutableStateFlow<List<ProductModel>>)
    fun getOptionList(model: OptionListRequestModel, stateFlow: MutableStateFlow<List<OptionModel>>)
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

    override fun getProductList(
        model: ProductListRequestModel,
        stateFlow: MutableStateFlow<List<ProductModel>>
    ) {
        val service: Retrofit? = RetrofitClient.getClient()
        service?.create(ServerCallInterface::class.java)
            ?.getProductList(model.toMap())
            ?.enqueue(object: retrofit2.Callback<ProductListResponseModel> {
                override fun onResponse(
                    call: Call<ProductListResponseModel>,
                    response: Response<ProductListResponseModel>
                ) {
                    if (response.isSuccessful) {
                        val body = response.body()
                        if (body != null) {
                            if (body.result == "Success") {
                                stateFlow.value = body.products
                            } else {
                                // TODO : fail 처리
                                Timber.d("getProductList body.result = ${body.result}, body.code = ${body.code}")
                            }
                        } else {
                            // TODO : fail 처리
                            Timber.d("getProductList Response Error")
                        }
                    } else {
                        // TODO : fail 처리
                        Timber.d("getProductList Response Failed")
                    }
                }

                override fun onFailure(call: Call<ProductListResponseModel>, t: Throwable) {
                    // TODO : fail 처리
                    Timber.d("getProductList onFailure - ${t.message}")
                }
            })
    }

    override fun getOptionList(
        model: OptionListRequestModel,
        stateFlow: MutableStateFlow<List<OptionModel>>
    ) {
        val service: Retrofit? = RetrofitClient.getClient()
        service?.create(ServerCallInterface::class.java)
            ?.getOptionList(model.toMap())
            ?.enqueue(object: retrofit2.Callback<OptionListResponseModel> {
                override fun onResponse(
                    call: Call<OptionListResponseModel>,
                    response: Response<OptionListResponseModel>
                ) {
                    if (response.isSuccessful) {
                        val body = response.body()
                        if (body != null) {
                            if (body.result == "Success") {
                                stateFlow.value = body.options
                            } else {
                                // TODO : fail 처리
                                Timber.d("getOptionList body.result = ${body.result}, body.code = ${body.code}")
                            }
                        } else {
                            // TODO : fail 처리
                            Timber.d("getOptionList Response Error")
                        }
                    } else {
                        // TODO : fail 처리
                        Timber.d("getOptionList Response Failed")
                    }
                }

                override fun onFailure(call: Call<OptionListResponseModel>, t: Throwable) {
                    // TODO : fail 처리
                    Timber.d("getOptionList onFailure - ${t.message}")
                }
            })
    }
}