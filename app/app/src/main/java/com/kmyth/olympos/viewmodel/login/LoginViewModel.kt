package com.kmyth.olympos.viewmodel.login

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.google.gson.Gson
import com.kmyth.olympos.network.RetrofitClient
import com.kmyth.olympos.network.ServerCallInterface
import com.kmyth.olympos.model.login.TableLoginRequestModel
import com.kmyth.olympos.model.login.TableLoginResponseModel
import com.kmyth.olympos.model.login.UserLoginRequestModel
import com.kmyth.olympos.model.login.UserLoginResponseModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import retrofit2.Call
import retrofit2.Response
import retrofit2.Retrofit
import timber.log.Timber

class LoginViewModel(
    private val repository: LoginRepository,
    private val userPreferencesRepository: UserPreferencesRepository
): ViewModel() {

    init {
        viewModelScope.launch(Dispatchers.Default) {
            userPreferencesRepository.fetchInitialPreferences()
        }
    }

    fun onUserLoginClick(userInfo: UserLoginRequestModel, navigate: (String) -> Unit) {
        Timber.d("onUserLoginClick")
        repository.userLogin(userInfo, navigate)
    }

    fun onTableLoginClick(tableInfo: TableLoginRequestModel, navigate: (Int) -> Unit) {
        Timber.d("onStoreLoginClick")
        repository.tableLogin(tableInfo, navigate)
    }
}

class LoginViewModelFactory(
    private val repository: LoginRepository,
    private val userPreferencesRepository: UserPreferencesRepository
): ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(LoginViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return LoginViewModel(repository, userPreferencesRepository) as T
        }

        throw IllegalArgumentException("Unknown ViewModel class :: ${modelClass::class.java.simpleName}")
    }
}

interface LoginRepository {
    fun userLogin(userInfo: UserLoginRequestModel, navigate: (String) -> Unit)
    fun tableLogin(tableInfo: TableLoginRequestModel, navigate: (Int) -> Unit)
}

class LoginRepositoryImpl: LoginRepository {
    override fun userLogin(userInfo: UserLoginRequestModel, navigate: (String) -> Unit) {
        val service: Retrofit? = RetrofitClient.getClient()
        service?.create(ServerCallInterface::class.java)
            ?.userLogin(userInfo)
            ?.enqueue(object: retrofit2.Callback<UserLoginResponseModel> {
                override fun onResponse(
                    call: Call<UserLoginResponseModel>,
                    response: Response<UserLoginResponseModel>
                ) {
                    if (response.isSuccessful) {
                        val body = response.body()
                        if (body != null) {
                            if (body.result == "Success") {
                                val storeStr = Gson().toJson(body.stores)
                                navigate(storeStr)
                            } else {
                                // TODO : fail 처리
                                Timber.d("userLogin body.result = ${body.result}, body.code = ${body.code}")
                            }
                        } else {
                            // TODO : fail 처리
                            Timber.d("userLogin Response Error")
                        }
                    } else {
                        // TODO : fail 처리
                        Timber.d("userLogin Response Failed")
                    }
                }

                override fun onFailure(call: Call<UserLoginResponseModel>, t: Throwable) {
                    // TODO : fail 처리
                    Timber.d("userLogin onFailure - ${t.message}")
                }
            })
    }

    override fun tableLogin(tableInfo: TableLoginRequestModel, navigate: (Int) -> Unit) {
        val service: Retrofit? = RetrofitClient.getClient()
        service?.create(ServerCallInterface::class.java)
            ?.tableLogin(tableInfo)
            ?.enqueue(object: retrofit2.Callback<TableLoginResponseModel> {
                override fun onResponse(
                    call: Call<TableLoginResponseModel>,
                    response: Response<TableLoginResponseModel>
                ) {
                    if (response.isSuccessful) {
                        val body = response.body()
                        if (body != null) {
                            if (body.result == "Success") {
                                navigate(tableInfo.store_uid)
                            } else {
                                // TODO : fail 처리
                                Timber.d("tableLogin body.result = ${body.result}, body.code = ${body.code}")
                            }
                        } else {
                            // TODO : fail 처리
                            Timber.d("tableLogin Response Error")
                        }
                    } else {
                        // TODO : fail 처리
                        Timber.d("tableLogin Response Failed")
                    }
                }

                override fun onFailure(call: Call<TableLoginResponseModel>, t: Throwable) {
                    // TODO : fail 처리
                    Timber.d("tableLogin onFailure - ${t.message}")
                }
            })
    }
}