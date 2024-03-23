package com.kmyth.olympos.viewmodel.product

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.kmyth.olympos.viewmodel.login.UserPreferencesRepository

class ProductViewModel(
    private val repository: ProductRepository,
    private val userPreferencesRepository: UserPreferencesRepository
): ViewModel() {
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
    fun etc() {
        //
    }
}

class ProductRepositoryImpl: ProductRepository {
    override fun etc() {
        super.etc()
    }
}