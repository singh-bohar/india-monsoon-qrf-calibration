import pandas as pd
import subprocess
import xarray as xr
import xskillscore
import numpy as np

# wk 1: leads 0-7 (7 days: L = 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5)
# wk 2: leads 7-14
# wk 3-4: leads 14-28
lead = (14, 28) 

# Large India domain: 70E-90E, 5N-35N
# weekly June starts 1989-2010 (training)
# weekly June starts 2011-2018 (validation)
west = 68
east = 98
south = 7 # for IMD data it do not work with 5 because data is starting from 6.5
north = 38
start_window = 'Jun-Sep'
training_years = (1989, 2014)  #for IITM-CFS (ERPv2) hindcast is ranging 2003-2018 there for for training 2003-2014
validation_years = (2015,2018)  # ERPv2 test 2015-2018

#Forecast start date 
day =7
month='Jun'   # first three letter of month first letter must be capital
year = 2024
#=======================================================================================================
##                                         IITM-CFSv2 (ERPv2) urls
#=======================================================================================================

#predictor_dataset_total_onemodel ='SOURCES/.IMD/.ERPv2/.r0p5/.CFS/.nsasfer/.hindcast/.APCPsfc/S/%28{first_year}-{final_year}%29VALUES/S/({start_window})/VALUES/Y/{south}/{north}/RANGE/X/{west}/{east}/RANGE/L/{lead_start}/{lead_end}/RANGEEDGES/%5B/L%5D//keepgrids/average//units/(mm/day)/def//name/(prcp)/def'

#predictor_dataset_total =predictor_dataset_total_onemodel

#predictor_dataset_total ='%5B/SOURCES/.IMD/.ERPv2/.r0p5/.CFS/.nsasfer/.hindcast/.APCPsfc/SOURCES/.IMD/.ERPv2/.r0p5/.CFS/.nsasfer_sc/.hindcast/.APCPsfc/SOURCES/.IMD/.ERPv2/.r0p5/.CFS/.nsaszc/.hindcast/.APCPsfc/SOURCES/.IMD/.ERPv2/.r0p5/.CFS/.nsaszc_sc/.hindcast/.APCPsfc/SOURCES/.IMD/.ERPv2/.r0p5/.CFS/.sasfer/.hindcast/.APCPsfc/SOURCES/.IMD/.ERPv2/.r0p5/.CFS/.saszc/.hindcast/.APCPsfc/%5D/%7B/S/%28{first_year}-{final_year}%29/VALUES/S/({start_window})/VALUES/Y/{south}/{north}/RANGE/X/{west}/{east}/RANGE/L/{lead_start}/{lead_end}/RANGEEDGES/%5BX/Y/S%5D/REORDER/%5BL%5D//keepgrids/average/%7D/forall/5/%7B/add/%7D/repeat/6./div///units/(mm/day)/def//name/(prcp)/def'

#=======================================================================================================
                                             #GEFS model's URL
#=======================================================================================================
predictor_dataset_total ='SOURCES/.Models/.SubX/.EMC/.GEFSv12_CPC/.hindcast/weekly/.pr/S/(0000%202%20Jan%20{first_year})/(0000%201%20Dec%20{final_year})/RANGEEDGES/S/7/STEP/S/({start_window})/VALUES/Y/{south}/{north}/RANGE/X/{west}/{east}/RANGE/L/{lead_start}/{lead_end}/RANGEEDGES/%5B/L%5D//keepgrids/average//units/(mm/day)/def//name/(prcp)/def'
predictor_dataset_total_onemodel =predictor_dataset_total 

forecast_dataset_total = 'SOURCES/.Models/.SubC/.EMC/.GEFSv12_CPC/.forecast/.pr/S/(0000%20{day}%20{month}%20{year})/VALUES/Y/{south}/{north}/RANGE/X/{west}/{east}/RANGE/L/{lead_start}/{lead_end}/RANGEEDGES/%5B/L%5D/average//units/(mm/day)/def//name/(prcp)/def'
#=======================================================================================================
#                                          predictand data sets urls
#=======================================================================================================
# CHIRPS data
predictand_dataset_total = 'SOURCES/.UCSB/.CHIRPS/.v2p0/.daily-improved/.global/.0p25/.prcp/Y/{south}/{north}/RANGE/X/{west}/{east}/RANGE'

#GPCP data (1997 onwards)
#predictand_dataset_total = 'SOURCES/.NASA/.GPCP/.V1DD/.V1p3/.precip/Y/{south}/{north}/RANGE/X/{west}/{east}/RANGE'

# IMD observational data 1989-2022
#predictand_dataset_total = 'SOURCES/.IMD/.RF0p25/.gridded/.daily/.v1989-2022/.rf/Y/{south}/{north}/RANGE/X/{west}/{east}/RANGE'

#=======================================================================================================
#                                   Final templates (do not change this)
#=======================================================================================================
predictor_url_template = f'https://iridl.ldeo.columbia.edu/{predictor_dataset_total}/L/removeGRID/data.nc'

predictand_url_template = f'https://iridl.ldeo.columbia.edu/{predictor_dataset_total_onemodel}/L/S/add/0/RECHUNK//name//T/def/2/%7Bexch%5BL/S%5D//I/nchunk/NewIntegerGRID/replaceGRIDstream%7Drepeat/use_as_grid/{predictand_dataset_total}/%5BX/Y%5D/regridLinear/T/(days%20since%201960-01-01)/streamgridunitconvert/T/{{lead_end}}/{{lead_start}}/sub/runningAverage/T/2/index/.T/SAMPLE/nip//name/(prcp)/def/data.nc'

forecast_url_template =f'https://iridl.ldeo.columbia.edu/{forecast_dataset_total}/data.nc'
#=======================================================================================================
#                                Functionality for downloading data set
#=======================================================================================================
def get_file(name, url_template, years, download,start_window):
    fname = f'./Week34/{name}_{start_window}_{years[0]}-{years[1]}.nc'
    dset_url = url_template.format(
        first_year=years[0],
        final_year=years[1],
        lead_start=lead[0],
        lead_end=lead[1],
        start_window=start_window,
        west=west,
        east=east,
        south=south,
        north=north,
    )
    if download:
        print(dset_url)
        subprocess.call(['curl','-b','/Users/bohar/cookies.txt','-k',dset_url, '-o',fname])
    
    da = xr.open_dataset(fname)['prcp']
    return da

def get_data(years, download):
    x = get_file('GEFS_pra', predictor_url_template, years, download,start_window)
    t = x['S'] + pd.Timedelta(days=(lead[0] + lead[1]) / 2)
    x = x.assign_coords(T=('S', t.values)).swap_dims(S='T')
    
    y = get_file('GEFS_CHIRPS_pra', predictand_url_template, years, download,start_window)

    assert (x['T'].values == y['T'].values).all()

    return x, y

def get_training(download=True):
    return get_data(training_years, download)


def get_validation(download=True):
    return get_data(validation_years, download)

def climo_predict(x):
    '''Predict function that always predicts climatological conditions,
    i.e. equal probabilities for all three terciles.'''
    x = x.mean('M')
    fcst = xr.concat(
        [xr.full_like(x, 1/3)] * 3,
        'category'
    ).where(x.notnull())
    return fcst

def rps(obs, fcst):
    # Put categorical observations in the shape of a forecast where
    # the probability of one tercile is 1 and the others are 0.
    obs_reshaped = xr.concat(
        [
            (obs == -1).assign_coords(category='below'),
            (obs == 0).assign_coords(category='normal'),
            (obs == 1).assign_coords(category='above'),
        ],
        'category'
    ).where(obs.notnull())
    return xskillscore.rps(obs_reshaped, fcst, dim='T', category_edges=None, input_distributions='p')

def rpss(reference, forecast, observations):
    return 1 - rps(observations, forecast) / rps(observations, reference)

def make_tercile_labeler(observations):
    edges = observations.quantile(q=[1/3, 2/3], dim='T')
    mask = (
        edges.isnull().any('quantile') |
        # degenerate points where there aren't enough unique
        # values to identify tercile
        (edges.isel(quantile=0) == 0) |
        (edges.isel(quantile=0) == edges.isel(quantile=1))
    )
    def labeler(y):
        return (
            xr.where(y < edges.isel(quantile=0), -1, 0) +
            xr.where(y > edges.isel(quantile=1), 1, 0)
        ).where(np.logical_not(mask))
    return labeler
#===================================================================================================
###                                  Get forecast data file
#===================================================================================================
def get_forecast_file(name, url_template, year, download):
    fname = f'./Week34/{name}_{day}_{month}_{year}.nc'
    dset_url = url_template.format(
        
        year=year,
        month=month,
        day=day,
        lead_start=lead[0],
        lead_end=lead[1],
        start_window=start_window,
        west=west,
        east=east,
        south=south,
        north=north,
    )
    if download:
        print(dset_url)
        subprocess.call(['curl','-b','/Users/bohar/cookies.txt','-k',dset_url, '-o',fname])
    
    da = xr.open_dataset(fname)['prcp']
    return da

def get_forecast_data(year, download):
    x = get_forecast_file('GEFS_pr_forecast', forecast_url_template, year, download)
    t = x['S'] + pd.Timedelta(days=(lead[0] + lead[1]) / 2)
    x = x.assign_coords(T=('S', t.values)).swap_dims(S='T')

    return x

def get_forecast(download=True):
    return get_forecast_data(year, download)
