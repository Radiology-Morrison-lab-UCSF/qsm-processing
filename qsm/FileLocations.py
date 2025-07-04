from typing import Union
import os

class FileLocations:

    def __init__(self, dir_dicoms_in, dir_out_top):
        self.dir_dicoms_in = dir_dicoms_in

        self.dir_out_top =dir_out_top
        self.dir_raw_nii = os.path.join(self.dir_out_top, 'raw/')
        
        
        self.dir_phase_mag = os.path.join(self.dir_out_top, 'phase_mag/')

        self.loc_phase = os.path.join(self.dir_phase_mag, 'phase.nii.gz')
        self.loc_magnitude = os.path.join(self.dir_phase_mag, 'magnitude.nii.gz')
        self.loc_TEs = os.path.join(self.dir_phase_mag, 'echo_times.txt')
        self.loc_brainmask = os.path.join(self.dir_out_top, "brainmask.nii.gz")
        self.loc_dicomHeader = os.path.join(self.dir_phase_mag, 'dicom_header.json')

        self.phase_unwrapped = os.path.join(self.dir_phase_mag, 'phase_corrected_unwrapped.nii.gz')
        self.romeo_mask = os.path.join(self.dir_phase_mag, 'romeo_mask.nii.gz')
        self.romeo_b0 = os.path.join(self.dir_phase_mag, 'romeo_b0.nii.gz')
              

        #self.dir_dicoms_out = os.path.join(dir_top, 'generated_dicoms/')


    def GetLoc(self, dir:str, echoNumber:Union[str,int], type:str, suffix:str="nii"):
        
        if int(echoNumber) < 10:
            echoNumber = "0" + str(echoNumber)
        else:
            echoNumber = str(echoNumber)

        loc = dir + "echo" + echoNumber + "_" +type+ "."+ suffix
        return loc