import numpy_financial as np

car_cost_GST = 65000.00
residual_value = 0.4688
novated_interest_rate = 0.03
lease_term = 3.00

PMT = (car_cost_GST - (car_cost_GST * residual_value)) * (novated_interest_rate / 12) / (
            1 - (1 + (novated_interest_rate / 12)) ** (-(lease_term * 12 - 2)))

print(PMT*12)


P = -(car_cost_GST - (car_cost_GST * residual_value))
r = novated_interest_rate / 12
n = (lease_term * 12) - 2

print(np.pmt(r, n, P)*12)

# =(PMT(B11/12,(12*B9)-2,-(B4-(B4*B7))))*12
