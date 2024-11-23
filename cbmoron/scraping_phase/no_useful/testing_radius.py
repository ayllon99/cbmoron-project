import numpy as np
'''This file has been used to calculate the most accurate radius distance to check if it is a shoot from three or two'''

proportion=647.39/361.89
center_top=50
center_left=10
center_top_scaled=center_top/proportion


def top_calculate(left_point,radius):
    top_point_scaled=np.sqrt((radius**2)-((left_point-center_left)**2))+center_top_scaled
    result=top_point_scaled*proportion
    return print(f'three_line= top:{result} left: {left_point}\nBottom= top: {100-result} left: {left_point}')


def left_calculate(top_point,radius):
    top_point=10
    top_point_esc=top_point/proportion
    left_point=np.sqrt((radius**2)-((top_point_esc-center_top_scaled)**2))+center_left
    return print(f'three_line= top:{top_point} left: {left_point}')

