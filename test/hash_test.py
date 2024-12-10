from app.geohash import address_sanity_check

def test_hash():
    sanity_check, geohash, box, query = address_sanity_check('chicago')
    assert geohash == 'dp3wnp1yffry'