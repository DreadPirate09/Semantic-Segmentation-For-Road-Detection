# Experimenting with U NET

#### I was blown away to see how good this model can perform with so few training samples (60 pieces)

<p align="center">
  <img src="README/u_net.PNG" width="45%" />
  <img src="README/u_net2.PNG" width="45%" />
</p>

##### As you can observe ,I excluded the map intentionally from the training masks data so we can use the gps feature in the self driving model
##### Here is a mask sample

<p align="center">
  <img src="README/mask_sample.bmp" width="45%" />
</p>


##### Looks like it works pretty well for lane marks (300 mask samples were used in the training process)

<p align="center">
  <img src="README/lane_u_net.PNG" width="45%" />
</p>
