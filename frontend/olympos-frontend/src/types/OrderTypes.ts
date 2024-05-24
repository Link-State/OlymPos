import type { RowData } from "./TableTypes";

export interface ResponseOrders extends RowData<null> {
    amount: number,
    last_modify_date: string,
    order_date: string,
    order_state: number,
    table_number: number,
    unique_order: number,
    unique_product: number,
    unique_store_info: number
}