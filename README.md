# An rMQR Code Generator
![Lorem_ipsum](https://user-images.githubusercontent.com/14174940/171996095-4707be09-506e-4ef2-ab90-9942d6efc2ed.png)

This is an rMQR Code image generetor implemented in Python.

## Important Notice
Please veryfy an image genereted by this software wheter it can decode correctry before use.

## Usage
```py
from rmqrcode import rMQR
import rmqrcode

data = "https://oudon.xyz"
qr = rMQR.fit(data, rmqrcode.ErrorCollectionLevel.M, fit_strategy=rmqrcode.FitStrategy.MINIMIZE_WIDTH)
```

----
The word "QR Code" is registered trademark of DENSO WAVE Incorporated.<br>
http://www.denso-wave.com/qrcode/faqpatent-e.html
