package com.kmyth.olympos

const val LOGIN_GRAPH_ROUTE = "login"

interface Routes {
    val route: String
}

object LoginNav: Routes {
    override val route: String
        get() = "login_screen"
}

object TableNav: Routes {
    override val route: String
        get() = "table_screen"
}

object ProductNav: Routes {
    override val route: String
        get() = "product_screen"
}