from typing import Any, Dict, List, Tuple

from shopeepy_wrapped.config.core import config
from shopeepy_wrapped.data.cleaning import clean_dataset
from shopeepy_wrapped.data.data_manager import save_dataset
from shopeepy_wrapped.parsing.parse_orders import generate_orders_df
from shopeepy_wrapped.parsing.parse_products import generate_products_df


class ShopeeInsights:
    def __init__(self, orders: Tuple[Dict]) -> None:
        # Parse Orders() and Products()
        orders_ = generate_orders_df(orders)
        products_ = generate_products_df(orders)

        df_orders = clean_dataset(dataframe=orders_, order_type=True)
        df_products = clean_dataset(dataframe=products_, order_type=False)

        self.orders = df_orders
        self.completed_orders = df_orders.loc[
            df_orders["order_status"] == "ORDER COMPLETED"
            ]
        self.products = df_products.merge(
            self.completed_orders[["order_id", "order_status"]], on="order_id"
        )
        self.insights: Dict = {}

        self.save_datasets()
        self.generate_insights()

    def save_datasets(self) -> None:
        save_dataset(
            file_name=config.data_config.CLEAN_ORDERS_DF_FILENAME, dataset=self.orders
        )
        save_dataset(
            file_name=config.data_config.CLEAN_PRODUCTS_DF_FILENAME,
            dataset=self.products,
        )

        return None

    def count_orders(self) -> None:
        try:
            orders_count = self.orders.groupby("order_status")["order_id"].count()

            self.update_insights_dict(
                ["cnt_orders_cancelled", "cnt_orders_completed", "total_checkouts"],
                [
                    orders_count["ORDER CANCELLED"],
                    orders_count["ORDER COMPLETED"],
                    orders_count["ORDER CANCELLED"] + orders_count["ORDER COMPLETED"],
                ],
            )
        except KeyError:
            pass
        return None

    def cnt_orders_by_day(self) -> None:
        try:
            count_orders_by_day_distrib = (
                self.completed_orders.groupby(self.completed_orders.order_placed.dt.day_name())[
                    "order_id"
                ]
                .count()
                .reset_index()
            )

            max_count_orders_by_day = count_orders_by_day_distrib["order_id"].max()

            days_with_most_orders_by_cnt = (
                count_orders_by_day_distrib["order_placed"]
                .loc[count_orders_by_day_distrib["order_id"] == max_count_orders_by_day]
                .tolist()
            )

            self.update_insights_dict(
                [
                    "count_orders_by_day_distrib",
                    "day_with_most_orders_by_cnt",
                    "max_count_orders_by_day",
                ],
                [
                    count_orders_by_day_distrib,
                    days_with_most_orders_by_cnt,
                    max_count_orders_by_day,
                ],
            )

        except KeyError:
            pass
        return None

    def cnt_orders_by_hour(self) -> None:
        try:
            count_orders_by_hr_distrib = (
                self.completed_orders.groupby(self.completed_orders.order_placed.dt.hour)[
                    "order_id"
                ]
                .count()
                .reset_index()
            )

            max_count_orders_by_hr = count_orders_by_hr_distrib["order_id"].max()

            hour_with_most_orders_by_cnt = (
                count_orders_by_hr_distrib["order_placed"]
                .loc[count_orders_by_hr_distrib["order_id"] == max_count_orders_by_hr]
                .tolist()
            )

            self.update_insights_dict(
                [
                    "count_orders_by_hr_distrib",
                    "hour_with_most_orders_by_cnt",
                    "max_count_orders_by_hr",
                ],
                [
                    count_orders_by_hr_distrib,
                    hour_with_most_orders_by_cnt,
                    max_count_orders_by_hr,
                ],
            )
        except KeyError:
            pass

        return None

    def sum_amt_orders_by_day(self) -> None:
        try:
            sum_amt_orders_by_day_distrib = (
                self.completed_orders.groupby(
                    self.completed_orders.order_placed.dt.day_name()
                )["order_total"]
                .sum()
                .reset_index()
            )

            max_amt_orders_by_day = sum_amt_orders_by_day_distrib["order_total"].max()

            most_expensive_day_by_amt_sum = (
                sum_amt_orders_by_day_distrib["order_placed"]
                .loc[
                    sum_amt_orders_by_day_distrib["order_total"]
                    == max_amt_orders_by_day
                    ]
                .tolist()
            )

            self.update_insights_dict(
                [
                    "sum_amt_orders_by_day_distrib",
                    "most_expensive_day_by_amt_sum",
                    "max_amt_orders_by_day",
                ],
                [
                    sum_amt_orders_by_day_distrib,
                    most_expensive_day_by_amt_sum,
                    max_amt_orders_by_day,
                ],
            )
        except KeyError:
            pass

        return None

    def avg_order_amt_per_day(self) -> None:
        try:
            avg_amt_orders_by_day_distrib = (
                self.completed_orders.groupby(
                    self.completed_orders.order_placed.dt.day_name()
                )["order_total"]
                .median()
                .reset_index()
            )

            max_avg_amt_orders_by_day = avg_amt_orders_by_day_distrib[
                "order_total"
            ].max()

            most_expensive_day_by_avg_amt = (
                avg_amt_orders_by_day_distrib["order_placed"]
                .loc[
                    avg_amt_orders_by_day_distrib["order_total"]
                    == max_avg_amt_orders_by_day
                    ]
                .tolist()
            )

            self.update_insights_dict(
                ["avg_amt_orders_by_day_distrib", "most_expensive_day_by_avg_amt"],
                [avg_amt_orders_by_day_distrib, most_expensive_day_by_avg_amt],
            )
        except KeyError:
            pass

        return None

    def avg_order_amt_per_hr(self) -> None:
        try:
            avg_amt_orders_by_hr_distrib = (
                self.completed_orders.groupby(
                    self.completed_orders.order_placed.dt.hour
                )["order_total"]
                .median()
                .reset_index()
            )

            max_avg_amt_orders_by_hr = avg_amt_orders_by_hr_distrib[
                "order_total"
            ].max()

            most_expensive_hr_by_avg_amt = (
                avg_amt_orders_by_hr_distrib["order_placed"]
                .loc[
                    avg_amt_orders_by_hr_distrib["order_total"]
                    == max_avg_amt_orders_by_hr
                    ]
                .tolist()
            )

            self.update_insights_dict(
                ["avg_amt_orders_by_hr_distrib", "most_expensive_hr_by_avg_amt"],
                [avg_amt_orders_by_hr_distrib, most_expensive_hr_by_avg_amt],
            )
        except KeyError:
            pass

        return None


    def get_avg_order_amt(self) -> None:
        try:
            avg_order_amt = self.completed_orders["order_total"].median()

            self.update_insights_dict(["avg_order_amt"], [avg_order_amt])
        except KeyError:
            pass

        return None

    def sum_voucher_savings(self) -> None:
        try:
            shopee_voucher_savings = self.completed_orders[
                "shopee_voucher_applied"
            ].sum()

            shop_voucher_savings = self.completed_orders["shop_voucher_applied"].sum()

            total_voucher_savings = shop_voucher_savings + shopee_voucher_savings

            self.update_insights_dict(
                [
                    "shopee_voucher_savings",
                    "shop_voucher_savings",
                    "total_voucher_savings",
                ],
                [shopee_voucher_savings, shop_voucher_savings, total_voucher_savings],
            )
        except KeyError:
            pass

        return None

    def most_expensive_product(self) -> None:
        try:
            completed_products = self.products.loc[
                self.products["order_status"] == "ORDER COMPLETED"
                ]

            most_exp_product_price = completed_products["product_price"].max()

            most_expensive_products = (
                completed_products["product_name"]
                .loc[completed_products["product_price"] == most_exp_product_price]
                .tolist()
            )

            self.update_insights_dict(
                ["most_expensive_products", "most_exp_product_price"],
                [[most_expensive_products], [most_exp_product_price]],
            )
        except KeyError:
            pass

        return None

    def products_aggregation(self) -> None:
        try:
            avg_product_amt = self.completed_orders["product_price"].median()

            self.update_insights_dict(["avg_product_amt"], avg_product_amt)
        except KeyError:
            pass

        self.most_expensive_product()

        return None

    def shipping_fees_agg(self) -> None:
        try:
            shipping_fee_no_discount = self.completed_orders.shipping_fee.sum()
            shipping_fee_discounts = (
                self.completed_orders.shipping_discount_subtotal.sum()
            )
            shipping_fee_with_discount = (
                    shipping_fee_no_discount - shipping_fee_discounts
            )

            self.update_insights_dict(
                [
                    "shipping_fee_no_discount",
                    "shipping_fee_discounts",
                    "shipping_fee_with_discount",
                ],
                [
                    shipping_fee_no_discount,
                    shipping_fee_discounts,
                    shipping_fee_with_discount,
                ],
            )
        except KeyError:
            pass

        return None

    def update_insights_dict(self, key_list: List[Any], value_list: List[Any]) -> None:
        len_list = len(key_list)

        for i in range(len_list):
            self.insights[key_list[i]] = value_list[i]

        return None

    def generate_insights(self) -> None:
        ###################
        # Orders by count #
        ###################

        self.count_orders()
        self.cnt_orders_by_day()
        self.cnt_orders_by_hour()

        ####################
        # Orders by amount #
        ####################

        self.sum_amt_orders_by_day()
        self.avg_order_amt_per_day()

        ######################
        # Orders aggregation #
        ######################

        self.get_avg_order_amt()

        ####################
        #  Voucher Savings #
        ####################

        self.sum_voucher_savings()

        ########################
        #  Product aggregation #
        ########################

        self.products_aggregation()

        ########################
        #     Shipping fees    #
        ########################

        self.shipping_fees_agg()
