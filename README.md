# Experimenting with U NET

<p align="center">
  <img src="unet.png" width="45%" />
</p>

#### I have to say that I was blown away to see how many features this model can retain with so few training samples ( 60 peaces )

<p align="center">
  <img src="u_net.PNG" width="45%" />
  <img src="u_net2.PNG" width="45%" />
</p>

##### as you can observe ,I excluded the map intentionally from the training masks data so we can use the gps feature in the self driving model
##### here is a mask sample

<p align="center">
  <img src="mask_sample.bmp" width="45%" />
</p>


##### Looks like it works pretty well for lane marks

<p align="center">
  <img src="lane_u_net.png" width="45%" />
</p>
