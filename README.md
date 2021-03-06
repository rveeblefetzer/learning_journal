# learning-journal

Extending a basic learning journal built with Pyramid and Postgres. For Code Fellows' Python 401 class.
Implements a login that is necessary for writing a new post or editing an existing one.


Uses [Start Bootstrap](http://startbootstrap.com/) - [Clean Blog](http://startbootstrap.com/template-overviews/clean-blog/)

Deployed at https://rv-learning-journal.herokuapp.com/

###Step 3 tox tests:
```
---------- coverage: platform darwin, python 2.7.13-final-0 ----------
Name                                       Stmts   Miss  Cover
--------------------------------------------------------------
learning_journal/__init__.py                  12      0   100%
learning_journal/models/__init__.py           22      3    86%
learning_journal/models/meta.py                5      0   100%
learning_journal/models/mymodel.py             9      0   100%
learning_journal/routes.py                     9      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      31     19    39%
learning_journal/security.py                  30     10    67%
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             61     38    38%
learning_journal/views/notfound.py             4      2    50%
--------------------------------------------------------------
TOTAL                                        183     72    61%
```

```
---------- coverage: platform darwin, python 3.6.0-final-0 -----------
Name                                       Stmts   Miss  Cover
--------------------------------------------------------------
learning_journal/__init__.py                  12      0   100%
learning_journal/models/__init__.py           22      3    86%
learning_journal/models/meta.py                5      0   100%
learning_journal/models/mymodel.py             9      0   100%
learning_journal/routes.py                     9      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      31     19    39%
learning_journal/security.py                  30     10    67%
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             61     38    38%
learning_journal/views/notfound.py             4      2    50%
--------------------------------------------------------------
TOTAL                                        183     72    61%
```

###Step 4/End of Week tox tests:
```
---------- coverage: platform darwin, python 2.7.13-final-0 ----------
Name                                       Stmts   Miss  Cover
--------------------------------------------------------------
learning_journal/__init__.py                  12      0   100%
learning_journal/models/__init__.py           22      3    86%
learning_journal/models/meta.py                5      0   100%
learning_journal/models/mymodel.py             9      0   100%
learning_journal/routes.py                     9      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      30     18    40%
learning_journal/security.py                  30     10    67%
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             56     15    73%
learning_journal/views/notfound.py             4      2    50%
--------------------------------------------------------------
TOTAL                                        177     48    73%
```

```
---------- coverage: platform darwin, python 3.6.0-final-0 -----------
Name                                       Stmts   Miss  Cover
--------------------------------------------------------------
learning_journal/__init__.py                  12      0   100%
learning_journal/models/__init__.py           22      3    86%
learning_journal/models/meta.py                5      0   100%
learning_journal/models/mymodel.py             9      0   100%
learning_journal/routes.py                     9      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      30     18    40%
learning_journal/security.py                  30     10    67%
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             56     15    73%
learning_journal/views/notfound.py             4      2    50%
--------------------------------------------------------------
TOTAL                                        177     48    73%
```

###Security tox tests
```
---------- coverage: platform darwin, python 2.7.13-final-0 ----------
Name                                       Stmts   Miss  Cover
--------------------------------------------------------------
learning_journal/__init__.py                  12      0   100%
learning_journal/models/__init__.py           22      0   100%
learning_journal/models/meta.py                5      0   100%
learning_journal/models/mymodel.py             9      0   100%
learning_journal/routes.py                     9      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      30     18    40%
learning_journal/security.py                  30      0   100%
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             44      0   100%
learning_journal/views/notfound.py             4      2    50%
--------------------------------------------------------------
TOTAL                                        165     20    88%
```

```
---------- coverage: platform darwin, python 3.6.0-final-0 -----------
Name                                       Stmts   Miss  Cover
--------------------------------------------------------------
learning_journal/__init__.py                  12      0   100%
learning_journal/models/__init__.py           22      0   100%
learning_journal/models/meta.py                5      0   100%
learning_journal/models/mymodel.py             9      0   100%
learning_journal/routes.py                     9      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      30     18    40%
learning_journal/security.py                  30      0   100%
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             44      0   100%
learning_journal/views/notfound.py             4      2    50%
--------------------------------------------------------------
TOTAL                                        165     20    88%
```

