import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/sign-in-sign-up/LoginView.vue'
import SignUpUserName from '@/views/sign-in-sign-up/SignUpUserName.vue'
import SignUpUserInfo from '@/views/sign-in-sign-up/SignUpUserInfo.vue'
import SignUpUserId from '@/views/sign-in-sign-up/SignUpUserId.vue'
import SignUpUserPw from '@/views/sign-in-sign-up/SignUpUserPw.vue'
import SignUpTerm from '@/views/sign-in-sign-up/SignUpTerm.vue'
import SignUpComplete from '@/views/sign-in-sign-up/SignUpComplete.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/login',
            component: Login,
        },
        {
            path: '/sign-up/user-name',
            component: SignUpUserName
        },
        {
            path: '/sign-up/user-info',
            component: SignUpUserInfo
        },
        {
            path: '/sign-up/user-id',
            component: SignUpUserId
        },
        {
            path: '/sign-up/user-pw',
            component: SignUpUserPw
        },
        {
            path: '/sign-up/term',
            component: SignUpTerm
        },
        {
            path: '/sign-up/complete',
            component: SignUpComplete
        },
        {
            path: '/',
            component: ()=>import('@/views/home/MainHome.vue'),
            redirect: '/store',
            children: [
                {
                    path: '/store',
                    name: 'store',
                    component: ()=>import('@/views/stores/StoresManagement.vue')
                },
                {
                    path: '/store/form/:storeId?',
                    component: ()=>import('@/views/stores/FormStore.vue')
                },
                {
                    path: '/menu',
                    name: 'menu',
                    component: ()=>import('@/views/menus/MenusManagement.vue'),
                },
                {
                    path: '/menu/group/:storeId?',
                    name: 'menuGroup',
                    component: ()=>import('@/views/menus/MenuGroupManagement.vue'),
                },
                {
                    path: '/order',
                    name: 'order',
                    component: ()=>import('@/views/orders/OrdersManagement.vue')
                },
                {
                    path: '/order-history',
                    name: 'order-history',
                    component: ()=>import('@/views/orders/OrderHistorys.vue')
                },
                {
                    path: '/sale',
                    name: 'sale',
                    component: ()=>import('@/views/sales/SalesManagement.vue')
                },
            ],
            beforeEnter: (to, from, next)=>{
                const accessToken = sessionStorage.getItem('access_token');
                if(!!! accessToken){
                    next('/login');
                }
                else {
                    next();
                }
            }
        },
    ]
});

export default router