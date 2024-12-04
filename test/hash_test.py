from app.geohash import address_sanity_check

def test_hash():
    sanity_check, geohash = address_sanity_check('chicago')
    assert geohash == 'dp3wnp1yffry'