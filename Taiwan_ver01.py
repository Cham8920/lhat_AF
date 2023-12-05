################################################
#####           PARAMETER SET-UP           #####
################################################
# Set-up of Landslide Hazard Assessment Tool (LHAT)
#
# The tool initialises and takes the following arguments
# necessary to parameterise both data preparation, alignment
# and data extraction steps.
# The following is a working example
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from lhat import IO as io

project = io.inputs(

    # Define a project name. This will be the name of the folder in which
    # your results are stored in
    project_name = 'Taiwan_test_ver13',

    # The crs defined here will dictate which crs your input data is reprojected
    # to, as well as your final result.
    #edited the reprojection(?)#epsg: 3857
    crs = 'epsg:3828',

    # Provide a path to your landslide points. This is COMPULSORY for the model
    # to work.
    #needs geojson -> point files
    landslide_points = './Projects/Taiwan_test/Input/LS_After_typhoon_Morakot.geojson',

    # Defining a random state (any integer) allows results to be reproducible
    random_state = 101,

    # A bounding box is required when taking inputs from online sources such as
    # geoservers. Use EPSG:4326 coordinates.

    #edited coords to Taiwan- works
    bbox = [[120.71649303255948,23.16524506593071],
            [120.92729320345792,23.16524506593071],
            [120.92729320345792,23.333691644220995],
            [120.71649303255948,23.333691644220995],
            [120.71649303255948,23.16524506593071]],

    # The following are inputs that are possible to use within LHAT.
    # 3 choices for filepaths are: your_file_path, 'online', None.
    #       your_file_path = path to the respective file in string
    #       'online'       = an online, typically global source is relied on instead.
    #                        For datasets that are calculated from another dataset
    #                        such as slope/aspect/roughness, leave as 'online'.
    #       None           = None as an argument means that the dataset is NOT
    #                        considered as input into the model.
    #
    # Data type is critical to define as categorical and numerical data undergo
    # different data treatments.
    #
    # For 'reference', take care that if an online dataset is used as the reference,
    # bbox arguments define the grid extent, while the pixel_size argument below
    # defines the resolution of your reference (and therefore, your output) dataset.
    inputs = {
        'dem': {'filepath': "./Projects/Taiwan_test/Input/dem_pc.tif",
        #'dem': {'filepath': 'online',
                'data_type': 'numerical'},
        #'slope': {'filepath': "./Projects/Taiwan_test/Input/slopeNan.tif",
        'slope': {'filepath': 'online',
                  'data_type': 'numerical'},#create
        #'aspect': {'filepath': "./Projects/Taiwan_test/Input/aspect.tif",
        'aspect': {'filepath': 'online',
                    'data_type': 'numerical'},#create
        #'lithology': {'filepath': 'online',
        #                'data_type': 'categorical'},
        #'Soil_M': {'filepath': 'online',
        #                'data_type': 'numerical'},#add categorical soil map
        #'river' :   {'filepath': "./Projects/Taiwan_test/Input/river.tif",
        #              'data_type': 'numerical'},#create proximity map              
        'prox_road': {'filepath': "./Projects/Taiwan_test/Input/Road_prox.tif",
                      'data_type': 'numerical'},#create proximity map
        'prox_river': {'filepath': "./Projects/Taiwan_test/Input/prox_river1.tif",
                        'data_type': 'numerical'},#create proximity map
        'reference': 'dem'
        },

    #no_data = [-9999, np.nan],
    no_data = -9999,  # Optional argument to define no_data value. Propogates
                        # for all processing of input files.

    pixel_size = 1000,    # Optional argument to define pixel size.
                          # Pixel size is only important for online datasets

    kernel_size = 3     # Define kernel size. Take into consideration pixel size
                        # and full extent of landslide-prone areas.
    )

######   Data Engineering Stage   ######
# The user has a choice to further refine the input data prior to running the
# model.
x, y = project.generate_xy()

print(x,y)


#x = x.drop(columns=['landslide_ids'])

# As an example
# for m in ['SVM', 'RF', 'LR']:
#     project.run_model(
#         x = x,
#         y = y,
#         model = m,
#         modelExist = False
#         )

project.run_model(

    x = x,
    y = y,
    model = 'LR',
    modelExist = False
    )

    