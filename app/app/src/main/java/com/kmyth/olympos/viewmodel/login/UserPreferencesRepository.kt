package com.kmyth.olympos.viewmodel.login

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import kotlinx.coroutines.flow.first

data class UserPreferences(
    val id: String,
    val pw: String,
    val storeId: Int,
    val tableId: Int
)

class UserPreferencesRepository(private val dataStore: DataStore<Preferences>) {
    private object PreferencesKeys {
        val USER_ID = stringPreferencesKey("user_id")
        val USER_PASSWORD = stringPreferencesKey("user_pw")
        val STORE_ID = intPreferencesKey("store_id")
        val TABLE_ID = intPreferencesKey("table_id")
    }

    suspend fun updateUserId(userId: String) {
        dataStore.edit { preferences ->
            preferences[PreferencesKeys.USER_ID] = userId
        }
    }

    suspend fun updateUserPw(userPw: String) {
        dataStore.edit { preferences ->
            preferences[PreferencesKeys.USER_PASSWORD] = userPw
        }
    }

    suspend fun updateStoreId(storeId: Int) {
        dataStore.edit { preferences ->
            preferences[PreferencesKeys.STORE_ID] = storeId
        }
    }

    suspend fun updateTableId(tableId: Int) {
        dataStore.edit { preferences ->
            preferences[PreferencesKeys.TABLE_ID] = tableId
        }
    }

    suspend fun fetchInitialPreferences() =
        mapUserPreferences(dataStore.data.first().toPreferences())

    private fun mapUserPreferences(preferences: Preferences): UserPreferences {
        val userId = preferences[PreferencesKeys.USER_ID] ?: ""
        val userPw = preferences[PreferencesKeys.USER_PASSWORD] ?: ""
        val storeId = preferences[PreferencesKeys.STORE_ID] ?: -1
        val tableId = preferences[PreferencesKeys.TABLE_ID] ?: -1
        return UserPreferences(userId, userPw, storeId, tableId)
    }
}