# reel-downloader

Instagram Reels, YouTube, TikTok, X (Twitter) ve Facebook başta olmak üzere birçok popüler platformdan yüksek kalitede video indirmenizi sağlayan, minimalist ve sade tasarımlı bir terminal (TUI) uygulamasıdır.

## Özellikler

* **Çoklu Platform Desteği:** YouTube, TikTok, Instagram, Facebook, X (Twitter) ve daha fazlası.
* **Akıllı Çerez (Cookie) Yönetimi:** Safari, Chrome, Firefox, Brave veya Edge tarayıcılarından çerezleri otomatik okuyarak korumalı/gizli hesap videolarını sorunsuz indirebilme.
* **Yerel Çerez Desteği:** Tarayıcı entegrasyonu yerine yerel bir `cookies.txt` dosyası algılandığında otomatik olarak onu kullanma.
* **Otomatik Birleştirme (Muxing):** Ayrı indirilen en yüksek kaliteli video ve ses izlerini arka planda `ffmpeg` ile otomatik olarak birleştirip tek bir MP4 dosyası üretme.
* **Minimalist Konsol Arayüzü:** Gereksiz emojilerden arındırılmış, profesyonel terminal renk paletine sahip, sade ilerleme çubuklu TUI tasarımı.

## Gereksinimler

* Python >= 3.10
* FFmpeg (Video/Ses birleştirme işlemleri için)
* Deno (YouTube imza çözme kararlılığı için)

macOS üzerinde gereksinimleri hızlıca kurmak için:
```bash
brew install ffmpeg deno python@3.12
```

## Kurulum ve Çalıştırma

1. Repoyu bilgisayarınıza klonlayın:
   ```bash
   git clone https://github.com/kullaniciadi/reel-downloader.git
   cd reel-downloader
   ```

2. Sanal ortam (venv) oluşturun ve paketleri yükleyin:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install yt-dlp instaloader curl_cffi
   ```

3. Uygulamayı başlatın:
   * **İnteraktif Mod (Link yapıştırarak):**
     ```bash
     ./indir.sh
     ```
   * **Doğrudan Link Vererek:**
     ```bash
     ./indir.sh "<video-linki>"
     ```

## macOS Güvenlik ve Yetki Çözümleri

macOS işletim sisteminde tarayıcı verilerine erişim kısıtlandığı için korumalı veya gizli hesaplarda indirme hatası alırsanız şu yöntemleri uygulayabilirsiniz:

1. **Terminal Uygulamasına İzin Verme (Safari için):**
   * *Sistem Ayarları -> Gizlilik ve Güvenlik -> Tam Disk Erişimi* ekranına gidin.
   * Kullandığınız Terminal uygulamasını (veya VS Code) aktif hale getirin.

2. **Manuel Çerez Dosyası Kullanma (En Kolay ve Garanti Çözüm):**
   * Tarayıcınıza `Get cookies.txt LOCALLY` benzeri bir cookie dışa aktarma eklentisi kurun.
   * İlgili video platformu (örn: Instagram) açıkken çerezlerinizi **Netscape** formatında dışa aktarın.
   * Dosyayı `cookies.txt` ismiyle bu projenin ana klasörüne kaydedin.
   * Program bu dosyayı algılayıp tarayıcı yetkisi istemeden doğrudan indirme yapacaktır.

## Geliştirici
Developed by **ilsdigital**
