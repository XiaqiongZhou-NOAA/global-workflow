#! /usr/bin/env bash
################################################################################
#   Script:    
#
source "${USHgfs}/preamble.sh"

outdirpre=${1}
varlist=${2}
dataformat=${3}
datares=${4}
datacompress=${5}
fhout_ocnice=${6}
cd "${outdirpre}" || true

nh=${FHMIN_GFS}
while [[ ${nh} -le ${FHMAX} ]];do
  fnh=$(printf "%3.3d" "${nh}")

  if [[ "${dataformat}" == "grib2" ]];then
    if [[ ${component_name} == "ocn" ]];then
      infile=${COM_OCEAN_GRIB}/${datares}/gefs.ocean.${cycle}.${datares}.f${fnh}.grib2
    fi
    if [[ ${component_name} == "ice" ]];then
      infile=${COM_ICE_GRIB}/${datares}/gefs.ice.${cycle}.${datares}.f${fnh}.grib2
    fi                                                                                                                                                                                                                                   
    oufile1=${outdirpre}/gefs.${component_name}.${cycle}.${datares}.f${fnh}.grib2
  fi

  if [[ "${dataformat}" == "netcdf" ]];then
    if [[ ${component_name} == "ocn" ]];then
      infile=${COM_OCEAN_NETCDF}/gefs.ocean.${cycle}.${datares}.f${fnh}.nc
    fi
    if [[ ${component_name} == "ice" ]];then
      infile=${COM_ICE_NETCDF}/gefs.ice.${cycle}.${datares}.f${fnh}.nc
    fi   
    oufile1=${outdirpre}/gefs.${component_name}.${cycle}.${datares}.f${fnh}.nc
  fi

  if [[ -f "${infile}" ]]; then #check if input file exists before extraction
    if [[ "${dataformat}" == "grib2" ]];then
      # shellcheck disable=SC2312
      ${WGRIB2} "${infile}" | grep -F -f "${varlist}" | ${WGRIB2} -i "${infile}" -append -grib "${oufile1}">/dev/null 
    fi
    if [[ "${dataformat}" == "netcdf" ]];then
      varsrequested=$(paste -s "${varlist}")
      varsinfile=$(cdo -showname "${infile}")
      varsavailable=""
      for i in ${varsrequested}; do
        #check if variable from parm file is available in netcdf file. If variable is not in netcdf file, do not try to extract that variable. 
        if [[ ${varsinfile} == *"${i}"* ]]; then
          varsavailable+="${i},"
        else
          echo "WARNING: ${i} is not available in ${infile}."
        fi
      done
      if [[ -z "${varsavailable}" ]];then
        echo "WARNING: No variables from parm file ${varlist} are available in netcdf file ${infile}."
      else
        ocnice_vars=${varsavailable::-1}
        ncks -v "${ocnice_vars}" "${infile}" "${oufile1}"
      fi
    fi  
    if [[ ${datacompress} -eq 1 ]];then
      bzip2 "${oufile1}" 
    fi 
  else
    echo "WARNING: ${infile} does not exist."
  fi

  nh=$(( nh + fhout_ocnice ))
done

exit 0                                                                                                                                                                                        