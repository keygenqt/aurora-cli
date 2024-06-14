from datetime import datetime

from aurora_cli.src.base.utils.app import app_language

text_title_en = 'Project plugins'
text_title_desc_en = 'Description'
text_title_number_en = 'Number of plugins'
text_title_aps_en = 'Platform-specific available for the Aurora OS platform'
text_title_ps_en = 'Platform-specific plugins'
text_title_nps_en = 'Non platform-specific plugins'

text_title_ru = 'Плагины проекта'
text_title_desc_ru = 'Описание'
text_title_number_ru = 'Количество плагинов'
text_title_aps_ru = 'Доступно для платформы ОС Аврора'
text_title_ps_ru = 'Платформо-зависимые плагины'
text_title_nps_ru = 'Платформо не зависимые плагины'

PLUGINS_OUTPUT_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{text_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body style="font-family: 'Open Sans', sans-serif;">
    <table cellpadding=0 style="
            max-width: 1000px;
            width: 100%;
            margin: 0 auto;
        ">
        <tr>
            <td style="
                width: 34%;
                vertical-align: top;
            ">
                <img style="
                    width: 100%;
                    border-radius: 20px;
                " alt="image" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAV4AAAFeCAYAAADNK3caAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9btSIVRTuIOGSoThbEijhqFYpQIdQKrTqYXPoFTRqSFBdHwbXg4Mdi1cHFWVcHV0EQ/ABxdnBSdJES/5cUWsR4cNyPd/ced+8Af73MVLNjAlA1y0gl4kImuyoEXxFAFwbQj5jETH1OFJPwHF/38PH1LsqzvM/9OXqVnMkAn0A8y3TDIt4gnt60dM77xGFWlBTic+Jxgy5I/Mh12eU3zgWH/TwzbKRT88RhYqHQxnIbs6KhEk8RRxRVo3x/xmWF8xZntVxlzXvyF4Zy2soy12mOIIFFLEGEABlVlFCGhSitGikmUrQf9/APO36RXDK5SmDkWEAFKiTHD/4Hv7s187FJNykUBzpfbPtjFAjuAo2abX8f23bjBAg8A1day1+pAzOfpNdaWuQI6NsGLq5bmrwHXO4AQ0+6ZEiOFKDpz+eB9zP6piwweAv0rLm9Nfdx+gCkqavkDXBwCIwVKHvd493d7b39e6bZ3w9exXKf5QqDRwAAAAZiS0dEALsAmwCMixwaYAAAAAlwSFlzAAAN1wAADdcBQiibeAAAAAd0SU1FB+gDBhIdEkd/fAkAACAASURBVHja7d1pdFTnnefx3711b1VpKbSBJGQhCTCLN2ww8Rpjg3fHa2y8Jpmek04mp8+cOZ0+eTmn38zMi5nOLJ30zLyZ06fT6QSvcRJ3HBInON7ikHg3ZnOMVpBAW0kq1Xa3eSEMhiowaCnV8v288aFKhYv/c+un5/7r3ucx9o4HgQAABWNSAgAgeAGA4AUAELwAQPACAAheACB4AQAELwAQvABA8AIACF4AIHgBAAQvABC8AACCFwAIXgAgeAEABC8AELwAAIIXAAheAADBCwAELwAQvAAAghcACF4AAMELAAQvAIDgBQCCFwAIXgAAwQsABC8AgOAFAIIXAEDwAgDBCwAELwCA4AUAghcAQPACAMELACB4AYDgBQCCFwBA8AIAwQsAIHgBgOAFABC8AEDwAgDBCwAgeAGA4AUAELwAQPACAAheACB4AYDgBQAQvABA8AIACF4AIHgBAAQvABC8AEDwAgAIXgAgeAEABC8AELwAAIIXAAheACB4AQAELwAQvAAAghcACF4AAMELAAQvAFQ2ixKUBieb0fCRfo0NHVYmmdD0ZFyuk6UwOPOsKhRSVe0SVcfqtKRhqZrbu1RVG6MwRcDYOx4ElKF4TYwe0/6339RQ934Fvk9BMCcNrSu0dtO1au1YJcMwKAjBi8/KpFP66A+vqG/fuxQD866prVMbvnir6pqWUQyCF5I0OTaiP+x8TsmJMYqBBWOGQtq07V61X7ieYhC8lW3s6BG98cIOefRvUSAbttypVZdcQSEK+UuPEhSPZGJSu3c+R+iioD54baeO9vdQCIK38viep907f6JMMkExUFhBoD/9+idKTk1QC4K3svR9vFcTw4MUAovCzWa0/63fUwiCt3I42az27f4dhcDi/vLf/57iI0cpBMFbGY72HaLFgKLQu/9DikDwVobBnoMUAUVh4OAe+b5HIQje8ua5rgYPHaAQKApOJqX4yDEKQfCWt3RyWr7nUggUjanxUYpA8Ja3TDpJEVBUUtNTFIHgLfdTuwxFQFHxHIciELzlzQ6HKQKKSsiyKQLBW97CVdUUAUUlWlNDEQjeMj/Iq6plmAwDikdtXSNFIHjLm2WH1dxxIYVAcRyP4YgamlspBMFb/tpWraMIKI5jcfXFCoXYEYzgrQCtnatlhSMUAouuY92lFIHgrQyRaJXWf2ELhcCiaulco6XL2ykEwVs5ui7aoOolDRQCixMEoZAuueYmCkHwVhbLDuuaOx/iGkosiiu23q0ljUspBMFbeZY0LtXm2x6QYTAsKJw1m65Xx5qLKUQBsdllERodOqzdO59TNjVNMbCAn35Dl1x7sy7csFmGYVAPghfTk3G9+8pOjQx0UwzMu5q6Rl1x051a1tZBMQhenG6ov1v7dr/CfmyYF5HqWl101Y1asfYShUIhCkLw4mwSE+M62t+jkcO9mhgZUiaZkOeyihTO8uE2TUWqahVrXKqm5SvU0rFK9Uub+Q6B4MVs/Ke/epwi4HNte+AJXX/rlyhEEeJXHwAQvABA8AIACF4AIHgBAAQvABC8AABJLDWPgqqqqlJjY6PCRbq7suM4mpiY0NTUFIMFghelr6mpSW1tbUX/PhsaGjQ8PKyhoSEGDQuCVgMKIhKJaPny5SXzfpctW6ba2loGDgQvSld9fX3JLT1YX1/PwIHgRemyrNLratk2u4GA4EUJy2QyvGeA4EUhxeNxeZ5XMu/X930NDw8zcCB4Ubpc11VPT48cxymJ99rX11cS7xWlicvJUDDJZFIHDx7UkiVLFA6HZZrF9Xs/CAJls1lNTk6W1OwcBC/wuafw8XicQqCi0WoAAIIXAAheAADBCwAELwCA4AUAghcoW0ZDh6xL75DZso5i4HNxHS8wp09QVOHNX1b4sq0y7LDke0q/82s5f3yS2oDgBeZbaO2Nil51r8wlSz9zDhlS9MrbJUNydhO+IHiBeWG2rFPk2u2y2tbk/wHDVHTT7VIQyPnjUxQMBC8wW0Z1o8LXPir7wk0yQp+zVq9hKnrlnTIMU9ndOygeCF7g/Ka4IdlX3KfIFTfLiJ7HdkCGocim2xQooO0Aghc41+AMrbxGkavvV6ihdZZ/B20HELzAueVlY5ci1z0ie8V6yZjjVZfH2w5B/Kjcg7+juCB4gVOEaxS+5hGF118nw5rHPdcMQ/alNxK8IHiBE8yQrEtuV2TT7TJrFmZ3Yau5U2bzWvnHDlJvghfAxIrblTLaFNpzQFYkonA0KisSkRUOn/ivaduybFvmbHdMNkOyL71ZmV0EL8ELVLiUGjUZa1P98nYd+O0r8t382/4YpiHDMGTZtsLVUUVrqxWpqZYdiShcXS27KirLtmVFo7IiYYXssKxwWCHblmEYM+2GrsuUCddK2QSFJ3iBSmVoIOhSKJlRbXOL1m27UQdfflWe4+b8ZOAHChQo62WUTWeUGJs4x4muqXA0qkhNVJHqKlnmxarSsGoUV0RxGQoYBoIXqBxxXaBR1aghk5Yk1ba0aO3WLTq461V5rjsv/w/f85WeTio9nTz+SFTSCkkrtERptWpIdRqQIZ8BqRCsToaK5ctWX9AuSXIz2ROP17a0aO3NWxSyFn5eMqmoDqpLH2uTsooxKAQvUN6Ggy4lNXPJmJPKKPBPzjhrm1u0dtsWhezCnBTGVa192qCUljIwBC9QnrKqVb+aT/zZyWQVBKee6te2zISvaYUK8p4yCumA1ilJ+BK8QDkaDFbK/czh7zmOAi+3x1rb3KJ1N99YkLbDzC+EkPZrvZJaxiARvED5mNYyDSr3Jgk3m83784VuO7gytV/rNK0WBovgBUpfIFP9QVfe5zzHOePrCt12cGXqgNYoQfgSvECpi2uF4ormfc4/S/Ce0nYo4Mz3gNYqoVYGrsxUxHW8nh/o6FhW8WlP0+lAyXRpXy+ZXPMwR+4s+H6gybEp1WdcZRxXqezJO9Qidkj+1KQ825QCXwp8GZYlIxKVEak+sUJZbfPx63zPcJPFvB+7MnRAa7RWpmI6wiASvMVvaCyrdz9J6g99GU1my+juoNZrOHJn1WcIFFsuxQzjxJ+D4w0IBZJnGpqaND5zPmjINCUr4igSdRSqmQngT9sOB37zinzPK0j4HtRqXaaEwppkHAneIj2dnHL18odTerU3wwjjJMPI+fPMI4Z0Mos/k3iBPE/ynEDZ6ZCsaUfRWl9WTdVM2+GWG2fucCvQzNfnRtOyUXY93u7BtP77r0YJXcz3ZFlOyldiVEqOOQoyqRNth0L1fEHwFqW3P07o+7+LK+Gw6AgWKIB9KTPlKjFuys9kTl7tEApRHFRe8H48kNK/vJVgnScUIH0lN+0rGZf8THpm5lugtR1A8BaNY+NZ/ePv+dIBheWkfaWnZ2a6sZZWrdl6A+GLygjeIJB+8U5CaY+5Lgo/880mXDmpmS/XYq2tWrPtBpkhLo9HmQfvJ4dT+uBYlpHE4mSvL6XjnnR8ZbNYS6vWFvAmCxC8i2LX3mlGEYvKzfjKpk7elBNradWam26Y/d5sIHiL2VTS075Rl1HEostMeZJ/8maKWGur1m67YZ6vdqCdRvAWge7BNCOIouBlfXnpU4/HmbYD1/mizIJ3MO4wgigKQSC5Tu7H6WTbget8USbBO5lkc0AUS/JKnpM/XGfaDtxkgTIJ3vEUwYvi4Z/lcKTtgLIJ3nDIYARRPJNe/+xfftF2QFkEb0M1F6qjeBjncNVBrLVVa7fOdicLJhoEbxGor+a0DcUj5J/bNeWfhi9tB4K3JHU024wgimO2a0iWEuf887HW422H8/rCjet4Cd4i0L4soih9XhRD8IYMWdHzmwjEWme+cKPnS/CWFNsydH1nlFHEIqeuZBkpGTX15/3SWAtth4o8ZPaOByV9/hKfcvVffjEil7OwotPgebomndLmZFKtrqtG31O955XdV0S+YSgVsZSMWAr5gSzPlyHJCAL5piHPmNlayDcMBYYh1zTkG4ackCHPNOWahlLptKb6jyjhOUr6M6+PhSxVG6ZChik38HV5db1qQ2Ue0KYhr86WWxeR0xhRYmW9ptrr5UbL699d8sErSbvendQL+5MkXZHocrL6i3hcV6eSfA+PeQnjxOWNGr56hdJ15XGGWxbB67iB/mnXqPayYM6iCgeBvjU+qjump2UGnIJg/gM4fn2rjl69Qn6Jr3lcFsErSYmUp3/41aiOcjfbomjyXP3tyLDWZcprk9HAkAx+hxSVzMpa9d+zTk5V6V7VVDZ3INRWhfStmxu1so5viBcjdP/X0GDZha5E6BajSHdCXTv2yE6V7iJZZXXrV33M0jdvadK17WGOzgK2F/52ZFjLPI9ioGCs4YxWvHBQpleaZ7hl02o4Xf+xjF54Z1IfjxMIC+k/jI3orkSCQmBRxLe0afDaDoK3mPiBNDiS0Z+PZPVWX1oDCUJ4PnU5Wf2foUG+SMMinrMb6v7m5SV3tUNZB+/peic/VPf0m/J9v6Rvvuzte6co3se//egWXTzawYcfiyqxsUn9t60pqfdcUbfLOJrUMffVkv931LYv/nuoSVfrorEVfOqx+J+H98dkbXFL6iYL1lXErKw7vFJGwO0RKAJ+oNjheEm9ZYIXs3LhEVoMKKJZ7yGCFxWgIbGEIqBohIdKa8kAghezEkvVUAQUDSteWjfvELyYlWg2QhFQPEGWLq0bKQhezEoykqYIKBp+tLSWCmD15RIy5lRrKFsrvwh+Xx6LZmg3oGi4TaW1TADBWwICGfr9RKc+STUVzXvaGw60mqFBkci01ZbU+6XVUALeSywvqtCVpF1NYwwMisbUygaCF/M72z0w3Vx07+vlpXE5Bmsfowg+I5ahRFtpXd5I8Ba5lG8pGxTfFwdTlqsXWkYZICy6yata5Nml9eUawVvkwqYns0hX4/7u6j6lQ8x6sYiz3Yip4c0XlNz7JniLnCVfnZHxonxvRyNZ/b8VRxgkLJqxre0luQUQwVsCrqrrV72VKsr39verBrSraZxBQsFNX9ao4Q3LS3RChaIXMVzd1bRfH6eWaiizRG6RrQr2Xze+o47dV+nCqRiDhYLIrKzV4dtWKzBKc4U8grdUBsrwdVH1MV1Ufawo398zd/5ZD7x5q9b3r2KwsLAz3csbdfiW1fKs0t3YllYD5kXWcvT0F3+plza+oYydpSCYd36NpeF7VqrvjrUlHbrMeDGvAiPQ7y96V++t2q8tezbr8u71LKaDOfOW2Jq8slkjly+XGymPyKqoPdf+PPmG3pn4vxzJhTqdCkx1HmvTmsNdapuqVm3WkuWWxkylunopO2wsykFjyDOXylsSVmZZtRKdDZpurinZXi4zXhT+1NDw1d0yoO6WAd13bFydU0mKgrOfNZm1+njLC+X/+4WhBgCCFwDKGq2GAnOCTvWkvyE3OP+7bVrsd9VoP0kRAYIX5xO6+5J/o2m/7rxfe4H9kRrtZygiQPDi3EO3S/uT35516HZE/6ckj0ICBC/Odaa7P/ltJWYdut+VFFBIgODFuYbuXNoLhC5A8OK8QrdL++bcXiB0F1t60tbg+/VKHIvK94rvQqCQ7SvWmlLb5XHZ1S4DRvDSXph96P4P0dNdfIljER3Y2SbPKe4rL5NjYY311Ojiu48oEnMYuCLHdbwL2F6YW0+X0F10gdT9WkvRh+6J4y5pqffNpYwbwVu5oTu3mS7thWKQmggrFS+t3Q0mBqrlO6wxQfBWXHvhb2gvlIlSmemeMkkPJM/lY13s6PEWzUz37yhikamqy8owpaCE9vMMV3uyo/zyZsZL6J7jTBfFJhT21XJJvKTe84ovjEpz7DR4QTODT/AWe+h20V4oYys2j6n5okkVe9/dDAXquHpETRdOzenv8RXTwex3lA3WM/i0Gop5pvttbo4oY4YZqOu6YS3fMK7p4YjcTPEt5G5HPdW2puelxTDiPqgRr0Nh52GtDv9nST4HAcFbbu0FQrdURGpdRWrL++YEN+hUr3ODJGnQXa9W64uqMV9l8Gk10F4AFsoR92GlgxpJUiBTh7JfJiII3uKZ6c59wRtCF8Ul7V+pAeeKUx6L+62Ke/dQHFoNpd5eoKeL4px/9ToPydOp/WtDvsLGUcrDjHdx2wv0dFGOJry7dMxbmXvcWh+p2vyjkv71FIngXbz2Aj1dlJtAtTrkfCnn8bCRVrv9Y6X8zdqT+UtlgsspFsFb+PZCYk53pBG6KE5H3SeU8BtyHu+035Bt9KrHeUiZoEp9zkOiMzl/qOQ5hO5835HmBiskzeZ6UF+W0cfAYJ6O71Xqda7NebzWHFez9Yzi3j0a8TqOB/RqtVo3K2b+isIRvAt5UHYtSHth1HlMH6dvU3Ce93Ua8rU++oLqbYIX82PAeUzZIHracRZolf2iJE+HnLs+05Iw1Z29S5dF35ChBMWj1TD/AtXM8ZKxvztD6D6qg+nbZxG6wfHQfZ7BwbxI+tdr0L045/GloR4tCe3UUfcrOZOOCb9FKZ9eL8G7QAxNa3n4T/PaXhh1HtPB9B2zeC+B1kd/TuhiHicWEfU49+dcPhaSo077p3KCLvU61+S8bok5oqi5hwISvAtnqf0vWhP9zby2F84/dH1CF/Nu3LtHo96KPMfwh6oy/6R+5zE5QSTnWOyyfyUppKPu1ykiwbvQ4fvSOYbud2kvoOj5alKPc2vO41EjqQusHUr4N2rIXZfz/LLjLYgh53H9ObtNaX8TxSR4FzJ8f3TWme/Zbo7on35cHyVpL6B4DDmP5P3CuMN+XSFjRL3OPfJzWhCuOu3n5ARr1OdeJV8h9TiPUEyCd3HaDmdrL/QlvqJ/GrtZHyQ8Oeexsh7tBSwUJ1itXje3dxszR9Vi/bPGvPs05rXlPN9uv6eo+a76ne1ygrAkacTrUNy7l6ISvIUN37O1F/oST+gH41vlSRrxpffPMXxpL2Ah9TpflXs8OD97zK0OPy8vaFRPdlveFkSbtUMJf6uG3LUnHg9kqMe5Xb7qKOwscB3veYavFCjptZ1xwZu+xBP6x/FTD+BRX/og4WlDbUi2SXsBhXd6cH6qxfpYMXOXDjv/XslgSc7zXfbvFDLG1ZO9O6cFkQ5q5QVLZRoTFJjgXejw/ZFkG2cI3a/oB+Nb875u5Hj4XlYbUtjM115gpouFESii7ux9Ck47wbWNrDrsZ5UN1qnX+ULO6+rMY1pqPaVR9yGNe8tznr/Ael+28YkCRWQoQ6FpNSz8oXy29sKZ5Gs70F7AQht1H9KE35LzeLv1tiLGHvVkn5AnO+cMbFX4Z/KDOvU4uZOJKiOhNutJTfm3qc/5a6KE4C28T9sL57IUztjx8M0eD1/aC1hIXtCmHuemnMsZq40pLbee0pR/q455q3Ne12odVK35so64X1EqqM3TgnhZpjGpnuxdGnA2KOlfQ7EJ3sIZz2zVD8a3nd8MxJf2THlaqV8QulhQg+7DSgWx3OAM75JpTOpQ9u6cULaMrFbYTysTXKx+Z9NZWhD3K+63yldIvc79Ck6bNYPgXTANkVf1QOyD83pNKAiUeu9tvf70kNLTtRQRCyIdXKF+Nzc4G0NH1Bj6iYbdhzXpL8t5vsN6SxFjn3qyj8s77WsgQ75Wh5+VFyxVt3PTicdHvA5NeHdTdIK3YCdzurT+e3oo9uE5v6LqvT8p8d4B7RkM6xdPbiR8sQAs9TsP5lw+ZspTp/2CvKD1xI7Cn1VjTqjVelKT3h0azrMrxXJrv2rM13XEfULp01oQh5zbKTvBW0iBLq3/e23/vJlvEKj2rdeUeP/giYc+/DR8k4Qv5s+Uv01H3Xy92wPHe7cndxQ+OZsN1Gm/LMNIqdu5K6cFYRsZrbCfUSa4TP3Oxpy/O2IkKTzBW/jwvaT+e3o49v6ZQ/ePu5R4Z69knFr2DwfDepHwxbwdiREdyt6b9/KxFfYOpfyrNeBsyHldQ+iIGkM/04i7XZP+0jwtiN0KGwfUnX0sbwuiy35eXtCibLCOQSB4C3vIX1z/fW1f8n5O6Fa9+Usldr8tWZG8r/zgSFi/fOoKZZI1lBFzMuw+ljc4O+03FTa61efcn3P5mClfXfbP5AYt6snbgoirxX5GE96XNOJ15jzfZu1TjfmGBtyvqc95nEEgeBdh5lv3fT38afgGgape/7lSr78hhWsl88zf/L5/OKIXn9pI+GLWZi4fuzFPcE6o1fqBJrw78+4ovNzapxrzVR1xHlEmqMppQXTZu2QorW7njjO0IHbMfJnnbNRR90Il/G0MBsG7CDPfuu/r4di7qnpzp1If9EjL1klV9ZJx9uUhCV/MxYD71bzBObOdj6lu586c18xcPvZjJf1rdNi9LOf5xtCAGkLPa9h9VFN+U56Z9B9kGz3qzj6qQObx1cvuUaBqBoTgXYy2wz/o/gv3SrXLJPPc785+/3BEv3x6ozIpwhfnLuVfpcNObnA2hfpUF3pRR93HNeU35jy/0n5dltGnPueBnN6tKU9d9k/lBp1n3BizxXpace/uUxZXj3utGnXvZ1AI3sWx7sq9euzOwfN+3XsDEe18eqMyKWYNOBeWep0v5wTnzFq6z8sN2tXjXJ83OJutHcd7tx05z7dZH6nafEOHne3KBNV5WhAvSfLU7Zy62H8gQ0e9zQwLwbvY4XvkvF/3bn9Ev3xqE+GLzxU/Y3DuUbX5R/U7T+TZzifQSnunDHk6lKd3GzbSard/rKR/vY64l+aZSferPvSCjrqPKuE35Hl+HwND8C52+O6b9cz3V88QvjgzX43qcW7PuXwsYiR1gf2Upv3rNOhelPO6paFe1YVe1JD7bzTt1+c832W/Jss4nHdjzJkbMX4iN+hUn5N/cfVm6znFvfuUCS5hkAjexZ35PnrH+YfvO30z4ZslfJHHsPtg3t5tp/2GLOOIepwHzrCdz0xw9uTp3cbMseMtiLvzb4x5Yib9mLJB9LSZtK8u+9eSfHU7d6jPeZRBOg3r8RbY+s179e+appVJnf+CIhOjDVrWzt1BOMkJVuft3S4xR9Rs7dC4d5/G82zn02btUZX5lj7J/se8u1KstP9VgWx9ks3dM3CmBfFDTfvXa9Bdn2cm3a/60C90xPmmEn6DEn6DWq3bFDN/zYARvItn+cpeioB5OWEdcB7JM+MM1GW/KD+IqcfZltO7jRpJXWA/qYS/5Qw7CndrSeglDTrfVDLI3dpnpf2qQsawerN/fYaZ9LPKBmvU71514vFD2Xu0Ifq6DDFxoNUAlLCkf7WOuJfkDc6Zy8e25+3ddtqvyzKOqde5Nyc4LcM5vqPwKvW5V+edSS+zdmjcu1ejXntuC8L+QFXm2xpwHjrlF8Kkv0wj7nYGjeAFSlu381DeGWdXeIcywSXqc79whuB8WmPevWfczidqvq0+57ETOwrntiAi6s7emvPaiJFUu/XPmvZvyNuCSPgXMGgEL1C6xrxHNOblBtkK+x1FjI804DyUc/nYTJvgRflBjXqy+VoQn27nc4uO5tkYszn0iZaEfqNB56t5N8Zcab8i0xhXt3Nfnl8InpbbOxm4T88sKAFQWnw1qjt7c97nhtyLNeZ9L+8iOZL0iXOPAt13hh2FX1PIGFVv5kvyT5uTWYajjvBzygZr1etcnffv7nOu02H3qry3FfsytT/zdZn6C60N/0BR821mvABKx6DzRN7glGa2XD9T6M6c7jdo2s/9wmxmO5+nNep+WeN+bgui3XpXUeN99TqP5twd96lkUJc3dKWZO9mm/CZN+M3qdR6q+G2CKix4DT61KGmZ4FL1u5vn+VMRaGX45/KCRvV+ZjufT1UZieMbY96io+6Fc/7/DXtdmvTuIHgrRcRk0RmUMksDzoN5e7dz0WJ9rJi5S0PudiVP2xhz5tK0T3cU/lLO3XGzEchQt3OHfMUI3kpQYzfx2UXJSvg3aijPl15zCwBPnfaPZ7bzca/M24Josp7VqPuAJvzmefv/TvlNGnYfqeBfoRWkIdymqNmstH+MTzFKTkgJXRx5btav73e2aiJnV2FDgWz1ZrfLDeycZ1aFn5cXNKnH2ZJzFUSVkdDq8E5J/uzCx0gQvJXAMExdEtuutyf+N59ilJwqc7eq5vD6sDGsd9N/dUqA+jK1L/OtvF+KtVoHVGP+Tn3Od3J2FJ7pC/9WDaFnGRhaDZ+vK/YFLQ1vYuRRcWrMN7Tc2pf3tP90tpFVh/0jpYONGnCuyNOCOKpGQpfgPefTNcPSdUu/oXrrIkYfFcbXCvsZ2Ubmc3+yw/qDwsYn6s1uz7uj8Krw8zLkUFKC99xFQzFtbfmO1tQ8KC4xQyUJG/vUYe3+nJlxXK32U5rw7tAxb1XO88ut/aoxX6GYc1Cxd67ZZkQbGx/QmtgWHUl9pJHMQSW9UXlBlqNiIeodOiSph0IUgRb7GQ15G/IuoDOzHsNLMpRRt3N3nhZERh32DykiwTs3tXaT1tpbtFZbOBoW0AWJZ6U4X2oWg5CGtdL+jT7KPJhzpUKtOab60L/qmPu1Myyu/qZso5si0moAcL7qQz9TY2gg5/GkX6dJ7+YzbozZYj1J8QheALNhyFGX/VOF5J3yuCdLe7OP5l1cfaX9a5mKUzyCF8BsVZtvaLn1Uc7jp28FJElNoT7VhV6kaAQvgLlqt3+ssJE+68/MbOfzMxnKUDCCF8Bc2UaPuuzXz/ozbdYeVZu/p1gEL4D50mz9SDFzLO9zESOldnsHRSJ4AcwnQymtsn8uQ0HOc532a7IMdsUmeAHMu1jot1oWOnTqY+aomq0fURyCF8DCzHodddo/kWU4x/8caFX453yhRvACWEhR821dYL0n6fiOwuZLFIXgBbDQ2qynFTPH1Bl+RrNd4Byfj+3dURCByaFWEoFg9OviyPcUNvYv0nFSGfuwMeNFQbjheopQIhYrdCXJja4ieIH5klzSRRHwuVJ1GwleYL5ML+mQF2XXD5zdZPOVBC8wXwLD1MjKv6QQOPNst+nLStRVxpkRVxXATQAAAU5JREFUwYuCGWvZpKnl36AQyOGFV+nI2q9VzL+X4EVBHVnzsKbaCF+c5FRvVt8V/03ZSF3F/JuNveNBwNCj0OpG9mlp9w8Vnn6TYlQo32pRfMXXNdK+RV4oUlH/doIXiyqaHFbV9KCsTFymx0aj5S4wQvLCMWWqlmk61q7ADFVkHQheACgwerwAQPACAMELACB4AYDgBQAQvABA8AIACF4AIHgBgOAFABC8AEDwAgAIXgAgeAEABC8AELwAQPACAAheACB4AQAELwAQvAAAghcACF4AIHgBAAQvABC8AACCFwAIXgAAwQsABC8AELwAAIIXAAheAADBCwAELwCA4AUAghcACF4AAMELAAQvAIDgBQCCFwBA8AIAwQsABC8AgOAFAIIXAEDwAgDBCwAgeAGA4AUAghcAQPACAMELACB4AYDgBQAQvABA8AJAZfr/OQDnWKM3YysAAAAASUVORK5CYII="/>
            </td>
            <td style="
                vertical-align: top;
                padding-left: 25px;
            ">
                <div style="margin-bottom: 10px;">
                    <div style="font-size: 28px; font-weight: 600;">
                        {text_title}
                    </div>
                    <div style="
                        font-weight: 700;
                        margin-bottom: 6px;
                        margin-top: 5px;
                        font-size: 15px;
                        color: #606060;
                    ">
                        {project_name}
                    </div>
                    <div style="font-size: 14px; color: #606060;">
                        {date_create}
                    </div>
                </div>
                <div style="margin-bottom: 10px;">
                    <div style="padding-bottom: 5px; font-weight: 800;">
                        {text_title_desc}
                    </div>
                    <div>
                        {description}
                    </div>
                </div>
                <div>
                    <div style="padding-bottom: 5px; font-weight: 800;">
                        {text_title_number}
                    </div>
                    <div>
                        {number_of_plugins}
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td colspan="2">
                <div style="
                    margin-top: 10px;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                    font-weight: 800;
                    font-size: 18px;
                    border-bottom: 1px solid #cfcfcf;
                ">
                    {text_title_aps}
                </div>
                <div>
                    <div>
                        <div style="
                            margin-bottom: 15px;
                            width: 100%;
                            background: #fefaf2;
                            border-radius: 8px;
                            padding: 16px;
                            box-sizing: border-box;
                        ">
                            <ol>
                                {items_plugins_ps_aurora}
                            </ol>
                        </div>
                    </div>
                </div>

                <div style="
                    margin-top: 10px;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                    font-weight: 800;
                    font-size: 18px;
                    border-bottom: 1px solid #cfcfcf;
                ">
                    {text_title_ps}
                </div>
                <div>
                    <div>
                        <div style="
                            margin-bottom: 15px;
                            width: 100%;
                            background: #f7fcf4;
                            border-radius: 8px;
                            padding: 16px;
                            box-sizing: border-box;
                        ">
                            <ol>
                                {items_plugins_ps}
                            </ol>
                        </div>
                    </div>
                </div>

                <div style="
                    margin-top: 10px;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                    font-weight: 800;
                    font-size: 18px;
                    border-bottom: 1px solid #cfcfcf;
                ">
                    {text_title_nps}
                </div>
                <div>
                    <div>
                        <div style="
                            margin-bottom: 15px;
                            width: 100%;
                            background: #f3f3f3;
                            border-radius: 8px;
                            padding: 8px;
                            box-sizing: border-box;
                        ">
                            <ol>
                                {items_plugins_dart}
                            </ol>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
    </table>
</body>
</html>
'''

PLUGINS_OUTPUT_HTML_ITEM = '''
<li style="padding-top: 4px;">
    <a style="color: black;" href="https://pub.dev/packages/{name}">{name}</a>
</li>
'''


def gen_flutter_report_plugins(
        name: str,
        description: str,
        find_plugins_nps: [],
        find_plugins_ps: [],
        find_plugins_aps: [],
) -> str:
    items_plugins_ps_aurora_h = []
    for plugin in find_plugins_aps:
        items_plugins_ps_aurora_h.append(PLUGINS_OUTPUT_HTML_ITEM.format(name=plugin))

    items_plugins_ps_h = []
    for plugin in find_plugins_ps:
        items_plugins_ps_h.append(PLUGINS_OUTPUT_HTML_ITEM.format(name=plugin))

    items_plugins_dart_h = []
    for plugin in find_plugins_nps:
        items_plugins_dart_h.append(PLUGINS_OUTPUT_HTML_ITEM.format(name=plugin))

    return PLUGINS_OUTPUT_HTML.format(
        text_title=text_title_ru if app_language() == 'ru' else text_title_en,
        text_title_desc=text_title_desc_ru if app_language() == 'ru' else text_title_desc_en,
        text_title_number=text_title_number_ru if app_language() == 'ru' else text_title_number_en,
        text_title_aps=text_title_aps_ru if app_language() == 'ru' else text_title_aps_en,
        text_title_ps=text_title_ps_ru if app_language() == 'ru' else text_title_ps_en,
        text_title_nps=text_title_nps_ru if app_language() == 'ru' else text_title_nps_en,
        project_name=name,
        date_create=datetime.now().strftime('%m/%d/%Y (%H:%M:%S)'),
        description=description,
        number_of_plugins=str(len(find_plugins_ps) + len(find_plugins_aps)),
        items_plugins_ps_aurora=''.join(items_plugins_ps_aurora_h) if items_plugins_ps_aurora_h else 'None',
        items_plugins_ps=''.join(items_plugins_ps_h) if items_plugins_ps_h else 'None',
        items_plugins_dart=''.join(items_plugins_dart_h) if items_plugins_dart_h else 'None',
    )
