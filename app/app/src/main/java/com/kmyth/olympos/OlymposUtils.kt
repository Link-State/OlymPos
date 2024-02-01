package com.kmyth.olympos

import android.content.Context
import android.provider.Settings

/**
 * SSAID 가져오기
 */
fun getSSAID(context: Context): String {
    return Settings.Secure.getString(context.contentResolver, Settings.Secure.ANDROID_ID)
}
