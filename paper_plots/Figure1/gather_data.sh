BASE_PATH=/home/moritz/hopfion_simulations/all_sp

# Criterion data, writes criterion_data.txt
# python3 ../../plot_criterion.py /home/moritz/hopfion_simulations/all_sp/* -data ./criterion_data.txt

## Isosurfaces around criterion plot
python3 ../../plot_spin_configuration.py /home/moritz/hopfion_simulations/all_sp/gamma_*_l0_3.000 -what hopfion -mode isosurface -view hopfion_normal -annotate 0 -distance 60 -background_color transparent -output_dir ./renderings -output_suffix _{gamma}_{l0}
python3 ../../plot_spin_configuration.py /home/moritz/hopfion_simulations/all_sp/gamma_1.000_l0_* -what hopfion -mode isosurface -view hopfion_normal -annotate 0 -distance 60 -background_color transparent -output_dir ./renderings -output_suffix _{gamma}_{l0}

## Schematic plot
# python3 ../../plot_spin_configuration.py /home/moritz/hopfion_simulations/all_sp/gamma_0.857_l0_5.000 -what hopfion -mode schematic -view hopfion_diagonal -annotate 0 -distance 220 -output_dir ./renderings -output_suffix _{gamma}_{l0}

## Cross_sections
# python3 ../../plot_spin_configuration.py ${BASE_PATH}/gamma_0.857_l0_5.000 -what hopfion -mode cross_section_ip -view hopfion_inplane -annotate 0 -distance 80 -output_dir ./renderings -output_suffix _{gamma}_{l0}
# python3 ../../plot_spin_configuration.py ${BASE_PATH}/gamma_0.857_l0_5.000 -what hopfion -mode cross_section_oop -view hopfion_normal -annotate 0 -distance 80 -output_dir ./renderings -output_suffix _{gamma}_{l0}

## Preimages_sections
# python3 ../../plot_spin_configuration.py ${BASE_PATH}/gamma_0.857_l0_5.000 -what hopfion -mode preimages -view hopfion_diagonal -annotate 0 -distance 65 -output_dir ./renderings -output_suffix _{gamma}_{l0}