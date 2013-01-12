##
import globalmaptiles as globaltiles
##
def latlng_to_zoompixels(mercator, lat, lng, zoom):
    mx, my = mercator.LatLonToMeters(lat, lng)
    pix = mercator.MetersToPixels(mx, my, zoom)
    return pix

def in_cluster(center, radius, point):
    return (point[0] >= center[0] - radius) and (point[0] <= center[0] + radius) \
       and (point[1] >= center[1] - radius) and (point[1] <= center[1] + radius)

def cluster_markers(mercator, latlngs, zoom, gridsize=50):
    """
    Args:
        mercator: instance of GlobalMercator()
        latlngs: list of (lat,lng) tuple
        zoom: current zoom level
        gridsize: cluster radius (in pixels in current zoom level)
    Returns:
        centers: list of indices in latlngs of points used as centers
        clusters: list of same length as latlngs giving assigning each point to
                  a cluster
    """
    centers = []
    clusters = []
    for i, (lat, lng) in enumerate(latlngs):
        point_pix = latlng_to_zoompixels(mercator, lat, lng, zoom)
        assigned = False
        for cidx, c in enumerate(centers):
            center = latlngs[c]
            center = latlng_to_zoompixels(mercator, center[0], center[1], zoom)
            if in_cluster(center, gridsize, point_pix):
                # Assign point to cluster
                clusters.append(cidx)
                assigned = True
                break
        if not assigned:
            # Create new cluster fo point
            centers.append(i)
            clusters.append(len(centers) - 1)
    return centers, clusters
##
if __name__ == '__main__':
    ##
    mercator = globaltiles.GlobalMercator()
    latlngs = [(28.43, 8), (28.43, 8), (28.44, 8), (35, 8)]
    centers, clusters = cluster_markers(mercator, latlngs, 21)
    ##
