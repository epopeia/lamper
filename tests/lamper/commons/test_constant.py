from lamper.commons import constant


def test_correct_pi():
    assert 3.14159265359 == constant.PI


def test_correct_gravity():
    assert 9.81 == constant.GRAVITY
