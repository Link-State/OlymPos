package com.kmyth.olympos.viewmodel.login

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.kmyth.olympos.model.login.UserLoginRequestModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

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
        repository.userLogin(userInfo, navigate)
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
}

class LoginRepositoryImpl: LoginRepository {
    override fun userLogin(userInfo: UserLoginRequestModel, navigate: (String) -> Unit) {
        // TODO
    }
}