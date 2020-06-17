import pandas as pd
import matplotlib.pyplot as plt

# These files are generated from the time series file in the Johns Hopkins GitHub
#https://github.com/CSSEGISandData/COVID-19/blob/master/who_covid_19_situation_reports/who_covid_19_sit_rep_time_series/who_covid_19_sit_rep_time_series.csv

infections = '/Users/fransvancoller/Desktop/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
deaths = '/Users/fransvancoller/Desktop/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
columns_to_skip = ["Lat", "Long"]

infections_global = pd.read_csv(infections,
                                usecols=lambda x: x not in columns_to_skip)
deaths_global = pd.read_csv(deaths,
                            usecols=lambda x: x not in columns_to_skip)

# Turning the pivot table into a csv that has dates as rows instead of columns
covid_infections = pd.melt(infections_global,
                           var_name="Date",
                           id_vars=["Country/Region", "Province/State"],
                           value_name="Confirmed Cases")
covid_deaths = pd.melt(deaths_global,
                       var_name="Date",
                       id_vars=["Country/Region", "Province/State"],
                       value_name="Deaths")

deaths_and_infections = pd.merge(covid_infections, covid_deaths,
                                 on=["Date", "Province/State", "Country/Region"])
deaths_and_infections["Date"] = deaths_and_infections["Date"].astype("datetime64[ns]")
deaths_and_infections = deaths_and_infections.loc[(deaths_and_infections["Country/Region"]=="Canada") &
                                                  (deaths_and_infections["Province/State"] == "Ontario")]

# I have all these defined even though I'm not using them in the charts below to view, I kind of just swtich between them
deaths_and_infections["Infections Growth"] = deaths_and_infections["Confirmed Cases"] - deaths_and_infections["Confirmed Cases"].shift(1)
deaths_and_infections["Death Growth"] = deaths_and_infections["Deaths"] - deaths_and_infections["Deaths"].shift(1)
deaths_and_infections["Infection Growth Rate"] = 100 * (deaths_and_infections["Confirmed Cases"] - deaths_and_infections["Confirmed Cases"].shift(1)) / deaths_and_infections["Confirmed Cases"].shift(1)
deaths_and_infections["Death Growth Rate"] = 100 * (deaths_and_infections["Deaths"] - deaths_and_infections["Deaths"].shift(1)) / deaths_and_infections["Deaths"].shift(1)
deaths_and_infections["Infected Died %"] = 100 * deaths_and_infections["Deaths"]/deaths_and_infections["Confirmed Cases"]
deaths_and_infections_date = deaths_and_infections[deaths_and_infections["Date"] >= "2020-04-01"]

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(deaths_and_infections_date["Date"], deaths_and_infections_date["Confirmed Cases"], "g-")
ax2.plot(deaths_and_infections_date["Date"], deaths_and_infections_date["Deaths"], "b-")

ax1.set_ylabel("Confirmed Cases", color="g")
ax2.set_ylabel("Deaths", color="b")

plt.show()
