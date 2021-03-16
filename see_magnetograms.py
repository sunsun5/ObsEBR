import functions

year = 2010
month = 2
day = 24

geo_data = functions.read_file(year, month, day)

for eix in ['EBRX', 'EBRY', 'EBRH', 'EBRZ', 'EBRF']:
    geo_data.plot(x='TIME', y=[eix], marker='.', markersize='4',
                  title=(f'{eix}\n' + geo_data['DATE'][0]),
                  legend=False)

d = functions.day_times(year, month, day)
print(f'Sunrise: {d[0][0]}\nNoon: {d[1][0]}\nSunset: {d[2][0]}')
