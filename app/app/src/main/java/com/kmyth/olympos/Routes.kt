package com.kmyth.olympos

interface Routes {
    val route: String
}

object Login: Routes {
    override val route: String
        get() = "login"
}

object Store: Routes {
    override val route: String
        get() = "store"
}

object Table: Routes {
    override val route: String
        get() = "table"
}