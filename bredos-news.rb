class BredosNews < Formula
  desc "BredOS news and system information utility"
  homepage "https://github.com/BredOS/news"
  url "https://github.com/BredOS/news.git",
      branch: "main"
  version "1.25.0"
  license "GPL-3.0"
  head "https://github.com/BredOS/news.git", branch: "main"

  depends_on "python@3.14"
  depends_on "smartmontools"

  resource "requests" do
    url "https://files.pythonhosted.org/packages/source/r/requests/requests-2.31.0.tar.gz"
    sha256 "942c5a758f98d790eaed1a29cb6eefc7ffb0d1cf7af05c3d2791656dbd6ad1e1"
  end

  resource "psutil" do
    url "https://files.pythonhosted.org/packages/source/p/psutil/psutil-5.9.6.tar.gz"
    sha256 "e4b92ddcd7dd4cdd3f900180ea1e104932c7bce234fb88976e2a3b296441225a"
  end

  def install
    # Get python3.14 path
    python3 = Formula["python@3.14"].opt_bin/"python3.14"
    
    # Create virtualenv in libexec
    system python3, "-m", "venv", libexec
    
    # Install dependencies
    system libexec/"bin/pip", "install", "--upgrade", "pip"
    system libexec/"bin/pip", "install", "requests", "psutil"

    # Install Python scripts
    libexec.install "client.py"
    libexec.install "server.py"

    # Create wrapper scripts
    (bin/"bredos-news").write <<~EOS
      #!/bin/bash
      exec "#{libexec}/bin/python" "#{libexec}/client.py" "$@"
    EOS

    (bin/"bredos-news-server").write <<~EOS
      #!/bin/bash
      exec "#{libexec}/bin/python" "#{libexec}/server.py" "$@"
    EOS

    chmod 0755, bin/"bredos-news"
    chmod 0755, bin/"bredos-news-server"

    # Install man page if it exists
    man1.install "bredos-news.1" if File.exist?("bredos-news.1")

    # Install LaunchAgent
    (prefix/"homebrew.mxcl.bredos-news.plist").write plist_text
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
        <key>EnvironmentVariables</key>
        <dict>
          <key>PATH</key>
          <string>#{Formula["smartmontools"].opt_sbin}:#{HOMEBREW_PREFIX}/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
        </dict>
      </dict>
      </plist>
    EOS
  end

  def caveats
    <<~EOS
      To start the bredos-news server automatically at login:
        brew services start bredos-news

      Or, if you don't want/need a background service:
        bredos-news-server

      Note: smartctl requires root privileges for disk access.
      The service may have limited functionality without sudo access.
      
      For full disk monitoring capabilities, you may need to:
      1. Run the server with sudo:
         sudo #{opt_bin}/bredos-news-server
      
      2. Or configure passwordless sudo for smartctl:
         echo "$(whoami) ALL=(ALL) NOPASSWD: #{Formula["smartmontools"].opt_sbin}/smartctl" | sudo tee /etc/sudoers.d/smartctl
         sudo chmod 0440 /etc/sudoers.d/smartctl

      To add bredos-news to your shell profile, add this to your ~/.zshrc or ~/.bash_profile:
        if command -v bredos-news &> /dev/null; then
          bredos-news
        fi
    EOS
  end

  test do
    system "#{bin}/bredos-news", "-p"
  end
end
