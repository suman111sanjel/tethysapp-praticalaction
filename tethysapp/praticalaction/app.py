from tethys_sdk.base import TethysAppBase, url_map_maker


class Praticalaction(TethysAppBase):
    """
    Tethys app class for Praticalaction.
    """

    name = 'Praticalaction'
    index = 'praticalaction:home'
    icon = 'praticalaction/images/icon.gif'
    package = 'praticalaction'
    root_url = 'praticalaction'
    color = '#16a085'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='praticalaction',
                controller='praticalaction.controllers.index'),
            UrlMap(
                name='chartHiwat',
                url='praticalaction/chartHiwat',
                controller='praticalaction.controllers.chartHiwat'),
            UrlMap(
                name='getGeoJson1',
                url='praticalaction/getGeoJson1',
                controller='praticalaction.controllers.getGeoJson1'),
            UrlMap(
                name='getForecastCSV',
                url='praticalaction/getForecastCSV',
                controller='praticalaction.controllers.getForecastCSV'),
            UrlMap(
                name='getHistoricCSV',
                url='praticalaction/getHistoricCSV',
                controller='praticalaction.controllers.getHistoricCSV'),
        )

        return url_maps