package com.kmyth.olympos.view.login

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Devices
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.kmyth.olympos.R
import com.kmyth.olympos.ui.theme.OlymPosTheme

@Composable
fun SelectScreen(
    title: String,
    selectList: List<String>,
    onClick: () -> Unit,
    modifier: Modifier
) {
    Box(
        modifier = modifier,
        contentAlignment = Alignment.Center
    ) {
        if (selectList.isEmpty()) {
            Column(
                modifier = Modifier
                    .width(width = 1280.dp)
                    .height(height = 480.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = title,
                    color = Color.Black,
                    textAlign = TextAlign.Center,
                    style = TextStyle(
                        fontSize = 64.sp
                    ),
                    modifier = Modifier
                        .padding(0.dp, 0.dp, 0.dp, 32.dp)
                        .wrapContentHeight(align = Alignment.CenterVertically)
                )
                Text(
                    text = stringResource(id = R.string.empty_select),
                    color = Color.Black,
                    textAlign = TextAlign.Center,
                    style = TextStyle(
                        fontSize = 36.sp
                    ),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(0.dp, 0.dp, 0.dp, 16.dp)
                        .wrapContentHeight(align = Alignment.CenterVertically)
                )
                Button(
                    modifier = Modifier
                        .width(width = 480.dp)
                        .height(height = 96.dp),
                    onClick = {  },
                    enabled = false
                ) {
                    Text(
                        text = stringResource(R.string.select),
                        fontSize = 32.sp
                    )
                }
            }
        } else {
            var expanded by remember { mutableStateOf(false) }
            var selectedText by remember { mutableStateOf(selectList[0]) }
            Column(
                modifier = Modifier
                    .width(width = 1280.dp)
                    .height(height = 480.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = title,
                    color = Color.Black,
                    textAlign = TextAlign.Center,
                    style = TextStyle(
                        fontSize = 64.sp
                    ),
                    modifier = Modifier
                        .padding(0.dp, 0.dp, 0.dp, 32.dp)
                        .wrapContentHeight(align = Alignment.CenterVertically)
                )
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
                        value = selectedText,
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
                        selectList.forEach { item ->
                            DropdownMenuItem(
                                text = {
                                    Text(
                                        text = item,
                                        fontSize = 36.sp
                                    ) },
                                onClick = {
                                    selectedText = item
                                    expanded = false
                                }
                            )
                        }
                    }
                }
                Button(
                    modifier = Modifier
                        .width(width = 480.dp)
                        .height(height = 96.dp),
                    onClick = onClick
                ) {
                    Text(
                        text = stringResource(R.string.select),
                        fontSize = 32.sp
                    )
                }
            }
        }
    }
}

@Preview(
    showBackground = true,
    showSystemUi = true,
    device = Devices.TABLET)
@Composable
fun SelectScreenPreview() {
    OlymPosTheme {
        SelectScreen(
            "Sample",
            listOf(),
            {},
            modifier = Modifier.fillMaxSize()
        )
    }
}