from integrations import github

def test_sample(): 
    assert 1 == 1

def test_validate_url():
    assert github.validate_url('https://github.com/chasemc67/TinyGen') == True