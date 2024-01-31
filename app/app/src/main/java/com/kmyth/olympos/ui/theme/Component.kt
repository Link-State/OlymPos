package com.kmyth.olympos.ui.theme

import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.material3.Button
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.LocalTextStyle
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * 기본 버튼
 */
@Composable
fun DefaultButton(title: String, enabled: Boolean, onClick: () -> Unit) {
    Button(
        modifier = Modifier
            .width(width = 480.dp)
            .height(height = 96.dp),
        onClick = onClick,
        enabled = enabled
    ) {
        Text(
            text = title,
            fontSize = 32.sp
        )
    }
}

/**
 * 기본 메뉴 박스
 */
@Composable
fun DefaultMenuBox(menuList: List<Pair<Int, String>>, callback: (Int) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    var selected by remember { mutableStateOf(menuList[0]) }
    ExposedDropdownMenuBox(
        expanded = expanded,
        onExpandedChange = {
            expanded = !expanded
        },
        modifier = Modifier
            .width(width = 480.dp)
            .padding(0.dp, 0.dp, 0.dp, 16.dp)
            .wrapContentHeight(align = Alignment.CenterVertically)
    ) {
        TextField(
            value = selected.second, // TODO
            onValueChange = {},
            readOnly = true,
            trailingIcon = {
                ExposedDropdownMenuDefaults.TrailingIcon(
                    expanded = expanded
                )
            },
            modifier = Modifier
                .menuAnchor()
                .fillMaxWidth(),
            textStyle = LocalTextStyle.current.copy(fontSize = 36.sp)
        )

        ExposedDropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            menuList.forEach { item ->
                DropdownMenuItem(
                    text = {
                        Text(
                            text = item.second, // TODO
                            fontSize = 36.sp
                        ) },
                    onClick = {
                        selected = item
                        expanded = false
                        callback(selected.first)
                    }
                )
            }
        }
    }
}