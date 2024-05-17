import DefaultAxios from '@/apis/DefaultApi';
import { ACCESS_TOKEN } from '@/functions/AccessToken';
import { push } from 'notivue';
import { API_CODE } from '@/constants/ApiCodeConstant';
import type { StoreId } from '@/types/StoreTypes';

const OrderHistoryApi = {
    getOrderList(params: StoreId){
        return DefaultAxios.get('/get-order-list', {
            params,
            headers: {
                Authorization: ACCESS_TOKEN()
            }
        })
        .then(res=>{
            if(res.data.code === 100 && res.data.result === "Success"){
                return res.data.orders;
            }
            else {
                throw new Error(res.data.code);
            }
        })
        .catch(error=>{
            throw new Error(API_CODE[error.message]);
        })
    },
}
export default OrderHistoryApi;