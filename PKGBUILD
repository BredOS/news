# Maintainer: Bill Sideris <bill88t@bredos.org>

pkgname=bredos-news
pkgver=1.2.2
pkgrel=2
pkgdesc='BredOS news and system information utillity'
arch=(any)
url=https://github.com/BredOS/sys-report
license=('GPL3')

depends=('python' 'python-aiohttp' 'python-psutil')
optdepends=('pacman-contrib: Show updatable packages' 'yay: Check for updatable development packages')

source=('99-bredos-news.sh' 'bredos-news.py')
sha256sums=('5dfa12531be0c234337321fb1f77a2569390f400c63888b02b45f1acbbf9f7e3'
            '752090aa289fce9efbe00d7fbbcd42a0f8a408bf05d8863805b0104775713356')

package() {
    mkdir -p "${pkgdir}/usr/bin" "${pkgdir}/etc/profile.d"
    install -Dm755 "${srcdir}/bredos-news.py" "${pkgdir}/usr/bin/bredos-news"
    install -Dm755 "${srcdir}/99-bredos-news.sh" "${pkgdir}/etc/profile.d/"
}
