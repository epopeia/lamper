from lamper import decorators



def test_post_decorator():

    def my_func(): ...

    dec = decorators.Mapping().post('/test')
    dec_func = dec(my_func)
    assert type(dec_func).__name__ == 'function'

def test_post_decorator():

    def my_func(): ...

    dec = decorators.Mapping().post('/test')
    dec_func = dec(my_func)
    assert type(dec_func).__name__ == 'function'

def test_put_decorator():

    def my_func(): ...

    dec = decorators.Mapping().put('/test')
    dec_func = dec(my_func)
    assert type(dec_func).__name__ == 'function'

def test_delete_decorator():

    def my_func(): ...

    dec = decorators.Mapping().delete('/test')
    dec_func = dec(my_func)
    assert type(dec_func).__name__ == 'function'

def test_patch_decorator():

    def my_func(): ...

    dec = decorators.Mapping().patch('/test')
    dec_func = dec(my_func)
    assert type(dec_func).__name__ == 'function'

def test_options_decorator():

    def my_func(): ...

    dec = decorators.Mapping().options('/test')
    dec_func = dec(my_func)
    assert type(dec_func).__name__ == 'function'