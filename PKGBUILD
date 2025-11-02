# Maintainer: Bill Sideris <bill88t@bredos.org>

pkgname=bredos-news
pkgver=1.22.1
pkgrel=1
pkgdesc='BredOS news and system information utility'
arch=('any')
url=https://github.com/BredOS/news
license=('GPL3')
groups=(bredos)
depends=('python' 'python-requests' 'python-psutil' 'python-pyinotify' 'smartmontools' 'mmc-utils-git' 'pacman-contrib')
optdepends=('yay: Check for updatable development packages')
makedepends=()
install=news.install

source=(
  'client.py'
  'server.py'
  '99-bredos-news.sh'
  'bredos-news-update.service'
  'bredos-news.1'
)

sha256sums=('624a5f85b0d2498de4ccd5517ee612c713c8e288e70fc5529758bbdabb309f74'
            'b8a79c4404ad6081dcd16e0e68489a7661d0f1666c463e926c3d830e6f471afe'
            '5dfa12531be0c234337321fb1f77a2569390f400c63888b02b45f1acbbf9f7e3'
            'c63d70907e9a2b1b96c4d618440ad10612822a8f18de2853af0a9402a868ec26'
            '0c8f13369aeedc0b2738f296f9c35e950e6043f28169c958762739e105e6a10e')

package() {
    install -d "$pkgdir/usr/bin"
    install -d "$pkgdir/usr/share/bredos-news"
    install -d "$pkgdir/usr/share/man/man1"
    install -d "$pkgdir/etc/profile.d"
    install -d "$pkgdir/usr/lib/systemd/system"

    # Main things
    install -m755 "$srcdir/client.py" "$pkgdir/usr/bin/bredos-news"
    install -m755 "$srcdir/server.py" "$pkgdir/usr/bin/bredos-news-server"

    # Service and manpage
    install -m644 "$srcdir/bredos-news-update.service" "$pkgdir/usr/lib/systemd/system/bredos-news-update.service"
    install -m644 "$srcdir/bredos-news.1" "$pkgdir/usr/share/man/man1/bredos-news.1"

    # Profile script
    install -m755 "$srcdir/99-bredos-news.sh" "$pkgdir/etc/profile.d/99-bredos-news.sh"
}
