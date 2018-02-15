

import netCDF4 as nc

def save_to_nc(data, nc_handle, exclude=None):
    """
    :param data: dict mapping str to ndarray
    :param nc_handle: netcdf file handle
    :param exclude: list of str
    :return: netcdf file handle
    """
    if exclude is None:
        exclude = []
    keys = [key for key in data.keys() if key not in exclude]

    # create dimensions
    for key in keys:
        for dim in data[key].shape:
            dim_name = "%d"%dim
            if dim_name not in nc_handle.dimensions.keys():
                nc_handle.createDimension( dim_name, dim)

    # create variables
    for key in keys:
        if data[key].dtype == int:
            store_format = "i8"
        elif data[key].dtype == float:
            store_format = "f8"
        else:
            raise RuntimeError("unsupported dtype %s"%data[key].dtype)

        dimensions = tuple([ "%d"%dim for dim in data[key].shape ])
        nc_handle.createVariable(key, store_format, dimensions)

    # save data
    for key in keys:
        nc_handle.variables[key][:] = data[key]
    return None
