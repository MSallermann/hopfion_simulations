export OMP_NUM_THREADS=4
nohup python3 hopfion_path.py -ii input_images/final_hopfion.ovf          -if input_images/intermediate_minimum_1.ovf -o second_im1 &
nohup python3 hopfion_path.py -ii input_images/intermediate_minimum_1.ovf -if input_images/intermediate_minimum_2.ovf -o second_im2 &
nohup python3 hopfion_path.py -ii input_images/intermediate_minimum_2.ovf -if input_images/ferromagnet.ovf            -o second_ferr &