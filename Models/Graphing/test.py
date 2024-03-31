from Organizer import Organizer
import numpy as np
from Plotter import Plotter

def main():
    #Loading Datasetsge
    PMF = np.genfromtxt("Examples/DNASE_CD14_positive_monocyte_female.txt", dtype=float, encoding=None, delimiter=",") 
    KF = np.genfromtxt("Examples/DNASE_keratinocyte_female.txt", dtype=float, encoding=None, delimiter=",") 
    start = 0
    end = 30
    dm = 0.03
    nd = 2
    hs = 5
    test_obj = Organizer(PMF, KF)
    test_obj.add_box("testbox0",
                     start, end,
                     dm, nd, hs, "blue")
    
    test_obj.add_box("testbox1",
                     60, 200,
                     0.02, 3, 4, "red")
    
    test_obj.add_box("testbox3",
                    400, 700,
                     0.02, 5, 3, "purple")
    
    print(test_obj.return_boxes())
    print(test_obj.return_dims())

    Plotter(test_obj)

    return


if __name__ == '__main__':
    main()