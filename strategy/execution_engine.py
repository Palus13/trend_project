from strategy.trend_module import detect_trend
from strategy.filters_module import check_filters


class ExecutionEngine:

    def __init__(self, df, params):

        self.df = df
        self.params = params

        self.position = 0
        self.entry_price = None
        self.entry_row = None

        self.capital = params["initial_capital"]

        self.contracts = params["contracts"]
        self.tick_value = params["tick_value"]

        self.daily_target = params["daily_target"]
        self.daily_stop = params["daily_stop"]

        self.daily_pnl = 0

        self.equity_curve = []
        self.trades = []
        self.daily_results = []

        self.current_trade_number = 0

    def close_trade(self, exit_row):

        points = (
            (exit_row["close"] - self.entry_price)
            if self.position == 1
            else (self.entry_price - exit_row["close"])
        )

        profit = points * self.tick_value * self.contracts

        self.capital += profit
        self.daily_pnl += profit

        trade_data = {
            "date": self.entry_row.name.date(),
            "trade_number_in_day": self.current_trade_number,
            "profit": profit,
            "points": points,
            "direction": self.position,
            "entry_hour": self.entry_row.name.hour,
            "entry_weekday": self.entry_row.name.weekday(),
            "entry_adx": self.entry_row["ADX"],
            "entry_slope": self.entry_row["MME_slope"],
            "entry_ma_distance": self.entry_row["MA_distance"],
            "entry_vol_exp": self.entry_row["vol_expansion"],
            "entry_bb_width": self.entry_row["bb_width"]
        }

        self.trades.append(trade_data)

        self.position = 0
        self.entry_price = None
        self.entry_row = None

    def run(self):

        previous_date = None
        trading_allowed = True

        for i in range(len(self.df)):

            row = self.df.iloc[i]
            current_date = row.name.date()
            current_hour = row.name.hour

            # ==========================
            # Novo dia
            # ==========================
            if previous_date is not None and current_date != previous_date:

                self.daily_results.append(self.daily_pnl)

                self.daily_pnl = 0
                trading_allowed = True
                self.current_trade_number = 0

                if self.position != 0:
                    self.close_trade(self.df.iloc[i - 1])

            previous_date = current_date

            # ==========================
            # Stop ou meta diária
            # ==========================
            if trading_allowed:
                if self.daily_pnl >= self.daily_target or self.daily_pnl <= -self.daily_stop:
                    trading_allowed = False
                    if self.position != 0:
                        self.close_trade(row)

            trend = detect_trend(self.df, i, self.params)

            if trading_allowed:

                if self.position == 0:

                    if trend != 0 and check_filters(self.df, i, self.params):

                        # 🔥 NOVA REGRA: NÃO OPERAR ANTES DAS 10h
                        if current_hour >= 10:

                            self.position = trend
                            self.entry_price = row["close"]
                            self.entry_row = row
                            self.current_trade_number += 1

                else:

                    if trend != 0 and trend != self.position:
                        self.close_trade(row)

                        if trading_allowed:

                            # Aplicar filtro horário também nas reversões
                            if current_hour >= 10:
                                self.position = trend
                                self.entry_price = row["close"]
                                self.entry_row = row
                                self.current_trade_number += 1

            self.equity_curve.append(self.capital)

        self.daily_results.append(self.daily_pnl)

        self.df["equity"] = self.equity_curve

        return self.df, self.trades, self.daily_results