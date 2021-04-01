import pandas as pd
import solaredge
import time

s = solaredge.Solaredge("YOUR-API-KEY")
site_id = YOUR-SITE-ID

# Edit this date range as you see fit
# If querying at the maximum resolution of 15 minute intervals, the API is limited to queries of a month at a time
# This script queries one day at a time, with a one-second pause per day that is polite but probably not necessary
day_list = pd.date_range(start="2019-12-01",end="2020-12-01")
day_list = day_list.strftime('%Y-%m-%d')

energy_df_list = []

for day in day_list:
    temp = s.get_energy_details(site_id,day+' 00:00:00',day +  ' 23:59:59',time_unit='QUARTER_OF_AN_HOUR')
    temp_df = pd.DataFrame(temp['energyDetails']['meters'][0]['values'])
    energy_df_list.append(temp_df)
    time.sleep(1)

power_df_list = []

for day in day_list:
    temp = s.get_power_details(site_id,day+' 00:00:00',day +  ' 23:59:59')
    temp_df = pd.DataFrame(temp['powerDetails']['meters'][0]['values'])
    power_df_list.append(temp_df)
    time.sleep(1)


energy_df = pd.concat(energy_df_list)
energy_df.columns = ['date','energy']
power_df = pd.concat(power_df_list)
power_df.columns = ['date','power']

merged = pd.merge(energy_df,power_df)

merged.to_csv("C:/merged_solar_data.csv",index=False)