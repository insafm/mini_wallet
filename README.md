* PipEnv is a way to create virtual environments in Python that allows for environment agnostic dependency installation.


Mini Wallet Exercise
--------------------------------------------------------


Installation Steps:
-----------------------------
- git clone https://github.com/insafm/mini_wallet.git

- cd mini_wallet

- python3 -m pip3 install pipenv

- python3 -m pipenv install --skip-lock

- python3 -m pipenv shell

- service postgresql start
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DATABASE NAME: test_mini_wallet
USER: postgres
PASSWORD: postgres
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- python3 manage.py migrate

- python3 manage.py runserver 0:7777


API Details:
--------------------------------------------------------

For authentication pass Token through header:

Authorization: Token <my token>

Routes:
--------------------------------------------------------
- POST - http://localhost/api/v1/init
- GET - http://localhost/api/v1/wallet [View my wallet balance]
- POST - http://localhost/api/v1/wallet [Enable my wallet]
- PATCH - http://localhost/api/v1/wallet [Disable my wallet]
- POST - http://localhost/api/v1/wallet/deposits [Add virtual money to my wallet]
- POST - http://localhost/api/v1/wallet/withdrawals [Use virtual money from my wallet]

--------------------------------------------------------

curl --location --request POST 'http://localhost:7777/api/v1/init' --form 'customer_xid="ea0212d3-abd6-406f-8c67-868e814a2436"'

Token: 0612b816365b78cbc1d7f3d108d2690c3153a825

curl --location --request POST 'http://localhost:7777/api/v1/wallet' --header 'Authorization: Token 0612b816365b78cbc1d7f3d108d2690c3153a825'

curl --location --request GET 'http://localhost:7777/api/v1/wallet' --header 'Authorization: Token 0612b816365b78cbc1d7f3d108d2690c3153a825'

curl --location --request PATCH 'http://localhost:7777/api/v1/wallet' --header 'Authorization: Token 0612b816365b78cbc1d7f3d108d2690c3153a825' --form 'is_disabled="true"'

curl --location --request POST 'http://localhost:7777/api/v1/wallet/deposits' --header 'Authorization: Token 0612b816365b78cbc1d7f3d108d2690c3153a825' --form 'amount="100000"' --form 'reference_id="50535246-dcb2-4929-8cc9-004ea06f5241"'

curl --location --request POST 'http://localhost:7777/api/v1/wallet/withdrawals' --header 'Authorization: Token 0612b816365b78cbc1d7f3d108d2690c3153a825' --form 'amount="60000"' --form 'reference_id="50535246-dcb2-4929-8cc9-004ea06f5241"'