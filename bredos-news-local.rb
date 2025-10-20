class BredosNewsLocal < Formula
  desc "BredOS news and system information utility (local development)"
  homepage "https://github.com/BredOS/news"
  url "file:///Users/panda/news-1"
  version "1.21.0-local"
  license "GPL-3.0"

  depends_on "python@3.11"

  resource "requests" do
    url "https://files.pythonhosted.org/packages/source/r/requests/requests-2.31.0.tar.gz"
    sha256 "942c5a758f98d790eaed1a29cb6eefc7ffb0d1cf7af05c3d2791656dbd6ad1e1"
  end

  resource "psutil" do
    url "https://files.pythonhosted.org/packages/source/p/psutil/psutil-5.9.6.tar.gz"
    sha256 "e4b92ddcd7dd4cdd3f900180ea1e104932c7bce234fb88976e2a3b296441225a"
  end

  def install
    # Install Python dependencies
    venv = virtualenv_create(libexec, "python3.11")
    venv.pip_install resources

    # Install Python scripts from current directory
    (libexec/"bin").install "client.py"
    (libexec/"bin").install "server.py"

    # Create wrapper scripts
    (bin/"bredos-news").write <<~EOS
      #!/bin/bash
      exec "#{libexec}/bin/python" "#{libexec}/bin/client.py" "$@"
    EOS

    (bin/"bredos-news-server").write <<~EOS
      #!/bin/bash
      exec "#{libexec}/bin/python" "#{libexec}/bin/server.py" "$@"
    EOS

    chmod 0755, bin/"bredos-news"
    chmod 0755, bin/"bredos-news-server"

    # Install man page if it exists
    man1.install "bredos-news.1" if File.exist?("bredos-news.1")

    # Install LaunchAgent
    (prefix/"homebrew.mxcl.bredos-news-local.plist").write plist_text
  end

  def plist_text
    <<~EOS
      <?xml version="1.0" encoding="UTF-8"?>
      <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
      <plist version="1.0">
      <dict>
        <key>Label</key>
        <string>#{plist_name}</string>
        <key>ProgramArguments</key>
        <array>
          <string>#{opt_bin}/bredos-news-server</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
        <key>KeepAlive</key>
        <true/>
        <key>StandardOutPath</key>
        <string>#{var}/log/bredos-news.log</string>
        <key>StandardErrorPath</key>
        <string>#{var}/log/bredos-news.error.log</string>
        <key>WorkingDirectory</key>
        <string>#{var}</string>
      </dict>
      </plist>
    EOS
  end

  def caveats
    <<~EOS
      To start the bredos-news server automatically at login:
        brew services start bredos-news-local

      Or, if you don't want/need a background service:
        bredos-news-server

      To add bredos-news to your shell profile, add this to your ~/.zshrc or ~/.bash_profile:
        if command -v bredos-news &> /dev/null; then
          bredos-news
        fi
    EOS
  end

  test do
    system "#{bin}/bredos-news", "--version"
  end
end
