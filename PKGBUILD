# Maintainer: Bill Sideris <bill88t@bredos.org>

pkgname=bredos-news
pkgver=1.2.8
pkgrel=1
pkgdesc='BredOS news and system information utility'
arch=(any)
url=https://github.com/BredOS/sys-report
license=('GPL3')

depends=('python' 'python-aiohttp' 'python-psutil')
optdepends=('pacman-contrib: Show updatable packages' 'yay: Check for updatable development packages')

source=('99-bredos-news.sh' 'bredos-news.py' 'cleanup-bredos-news.hook')
sha256sums=('5dfa12531be0c234337321fb1f77a2569390f400c63888b02b45f1acbbf9f7e3'
            '98e4cb4eec5432b47c17b678115c5ee747861e6dcbda66cba334e96ee3075168'
            'b57a96cb472b440a0500680552845b04443578265ceb1ed7dba2ff8f86b66b33')

package() {
    mkdir -p "${pkgdir}/usr/bin" "${pkgdir}/etc/profile.d" "${pkgdir}/etc/pacman.d/hooks/cleanup-bredos-news.hook"
    install -Dm755 "${srcdir}/bredos-news.py" "${pkgdir}/usr/bin/bredos-news"
    install -Dm755 "${srcdir}/99-bredos-news.sh" "${pkgdir}/etc/profile.d/"
    install -Dm644 "${srcdir}/cleanup-bredos-news.hook" "${pkgdir}/usr/share/libalpm/hooks/cleanup-bredos-news.hook"
}
