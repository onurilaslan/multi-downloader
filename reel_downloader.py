#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import glob
import argparse
import http.cookiejar

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"

BROWSER_MAP = {
    "1": "safari",
    "2": "chrome",
    "3": "firefox",
    "4": "edge",
    "5": "brave",
    "6": None
}

def log_info(msg):
    print(f"{CYAN}[i] BİLGİ:{RESET} {msg}")

def log_success(msg):
    print(f"{GREEN}[+] BAŞARILI:{RESET} {BOLD}{msg}{RESET}")

def log_warn(msg):
    print(f"{YELLOW}[!] UYARI:{RESET} {msg}")

def log_error(msg):
    print(f"{RED}[-]{RESET} {BOLD}{msg}{RESET}")

def get_local_cookies_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cookie_file = os.path.join(script_dir, "cookies.txt")
    if os.path.exists(cookie_file):
        return cookie_file
    return None

def detect_platform(url):
    url_lower = url.lower()
    if "instagram.com" in url_lower:
        return "instagram"
    elif "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    elif "tiktok.com" in url_lower:
        return "tiktok"
    elif "twitter.com" in url_lower or "x.com" in url_lower:
        return "twitter_x"
    elif "facebook.com" in url_lower or "fb.watch" in url_lower:
        return "facebook"
    return "generic"

def extract_shortcode(url):
    pattern = r"(?:https?://)?(?:www\.)?instagram\.com/(?:reel|reels|p)/([^/?#&]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def print_banner():
    banner = f"""{MAGENTA}
   __   __ _       _                   ___            _ _     _      _ 
   \\ \\ / /(_)   __| |  ___   ___      |_ _| _ _   __| (_) __ (_) ___(_)
    \\ V / | |  / _` | / -_) / _ \\      | | | ' \\ / _` | |/ _|| |/ _/| |
     \\_/  |_|  \\__,_| \\___| \\___/     |___||_||_\\__,_|_|\\__||_|\\__\\|_|
                                                                     {RESET}"""
    print(banner)
    print(f"                 {BOLD}{CYAN}// Developed by {MAGENTA}ilsdigital{RESET}")
    print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

def print_permission_instruction(browser, error_msg):
    print(f"\n{BOLD}{RED}┌────────────────────────────────────────────────────────┐")
    print(f"│            macOS GÜVENLİK VE YETKİ ENGELİ              │")
    print(f"└────────────────────────────────────────────────────────┘{RESET}")
    print(f"{RED}Sistem, {BOLD}{browser.upper()}{RESET}{RED} tarayıcısının çerezlerine erişemedi.{RESET}")
    print(f"Hata detayı: {error_msg}\n")
    print(f"{BOLD}{CYAN}Çözüm Yolları:{RESET}")
    print(f"  {BOLD}{MAGENTA}1.{RESET} Başka Bir Tarayıcı Deneyin:")
    print(f"     Instagram hesabınızın açık olduğu başka bir tarayıcı (Chrome, Firefox vb.) seçin.")
    print(f"  {BOLD}{MAGENTA}2.{RESET} Terminale Yetki Verin (Safari için):")
    print(f"     macOS Sistem Ayarları -> Gizlilik ve Güvenlik -> Tam Disk Erişimi (Full Disk Access)")
    print(f"     altından kullandığınız Terminal / VS Code uygulamasına izin verin.")
    print(f"  {BOLD}{MAGENTA}3.{RESET} Manuel Çerez Dosyası Kullanın (En Kolay ve Kesin Çözüm):")
    print(f"     - Tarayıcınıza 'Get cookies.txt LOCALLY' eklentisini kurun.")
    print(f"     - Instagram açıkken çerezleri Netscape formatında dışa aktarın.")
    print(f"     - İndirdiğiniz dosyayı {BOLD}cookies.txt{RESET} ismiyle bu projenin klasörüne ({os.getcwd()}) kaydedin.")
    print(f"     - Program bu dosyayı otomatik algılayacak ve yetki istemeden indirme yapacaktır.")
    print(f"{BOLD}{RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")

def print_video_info_box(platform, detail_label, detail_val):
    print(f"\n{BOLD}{CYAN}╔════════════════════════════════════════════════════════════════════════╗")
    print(f"║ [ VİDEO BİLGİLERİ ]{RESET}")
    print(f"╠════════════════════════════════════════════════════════════════════════╣")
    print(f"║ {BOLD}Platform:{RESET} {MAGENTA}{platform.upper()}{RESET}")
    print(f"║ {BOLD}{detail_label}:{RESET} {detail_val}")
    print(f"╚════════════════════════════════════════════════════════════════════════╝{RESET}\n")

def print_success_box(saved_path):
    print(f"\n{BOLD}{GREEN}╔════════════════════════════════════════════════════════════════════════╗")
    print(f"║ [ İNDİRME BAŞARILI ]{RESET}")
    print(f"╠════════════════════════════════════════════════════════════════════════╣")
    print(f"║ {BOLD}Kaydedilen Konum:{RESET} {saved_path}")
    print(f"╚════════════════════════════════════════════════════════════════════════╝{RESET}\n")

def create_progress_hook():
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '').replace('%', '').strip()
            speed = d.get('_speed_str', '').strip()
            eta = d.get('_eta_str', '').strip()
            try:
                percent_val = float(percent_str)
            except ValueError:
                percent_val = 0.0
            bar_length = 20
            filled_length = int(round(bar_length * percent_val / 100))
            bar = f"{CYAN}{'█' * filled_length}{RESET}{MAGENTA}{'░' * (bar_length - filled_length)}{RESET}"
            print(f"\r{MAGENTA}>{RESET} İndiriliyor: ▕{bar}▏ {BOLD}{percent_str}%{RESET} | Hız: {CYAN}{speed}{RESET} | Kalan: {YELLOW}{eta}{RESET}    ", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\r{GREEN}[+] {RESET}Dosya indirme bitti, birleştirme/disk işlemleri yapılıyor...          \n")
    return progress_hook

def download_with_ytdlp(url, out_dir, shortcode, browser=None):
    try:
        import yt_dlp
    except ImportError:
        log_warn("yt-dlp kütüphanesi yüklenemedi. instaloader alternatifi deneniyor...")
        return False
    log_info("yt-dlp ile indirme başlatılıyor...")
    out_tmpl = os.path.join(out_dir, f"instagram_reel_{shortcode}.%(ext)s")
    class MyLogger:
        def debug(self, msg):
            pass
        def warning(self, msg):
            pass
        def error(self, msg):
            pass
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': out_tmpl,
        'logger': MyLogger(),
        'progress_hooks': [create_progress_hook()],
        'quiet': True,
        'no_warnings': True,
    }
    local_cookies = get_local_cookies_file()
    if local_cookies:
        log_info("Çerezler yerel 'cookies.txt' dosyasından okunuyor...")
        ydl_opts['cookiefile'] = local_cookies
    elif browser:
        log_info(f"Çerezler '{browser}' tarayıcısından aktarılıyor...")
        ydl_opts['cookiesfrombrowser'] = (browser, None, None, None)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        expected_file = os.path.join(out_dir, f"instagram_reel_{shortcode}.mp4")
        if os.path.exists(expected_file):
            return expected_file
        return False
    except Exception as e:
        error_msg = str(e)
        if "Operation not permitted" in error_msg or "Permission denied" in error_msg:
            print_permission_instruction(browser or "browser", error_msg)
        else:
            log_warn(f"yt-dlp ile indirme başarısız oldu: {e}")
        return False

def download_with_instaloader(shortcode, out_dir, browser=None):
    try:
        import instaloader
    except ImportError:
        log_error("instaloader kütüphanesi yüklü değil!")
        return False
    log_info("Alternatif yöntem (instaloader) başlatılıyor...")
    loader = instaloader.Instaloader(
        download_pictures=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        dirname_pattern=out_dir,
        filename_pattern=f"instagram_reel_{shortcode}"
    )
    local_cookies = get_local_cookies_file()
    if local_cookies:
        try:
            log_info("Çerezler 'cookies.txt' dosyasından instaloader'a yükleniyor...")
            cj = http.cookiejar.MozillaCookieJar(local_cookies)
            cj.load(ignore_discard=True, ignore_expires=True)
            loader.context._session.cookies.update(cj)
        except Exception as ce:
            log_warn(f"instaloader, 'cookies.txt' dosyasını okuyamadı: {ce}")
    try:
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=out_dir)
        expected_file = os.path.join(out_dir, f"instagram_reel_{shortcode}.mp4")
        clean_pattern = os.path.join(out_dir, f"instagram_reel_{shortcode}.*")
        for f in glob.glob(clean_pattern):
            if not f.endswith(".mp4"):
                try:
                    os.remove(f)
                except OSError:
                    pass
        if os.path.exists(expected_file):
            return expected_file
        return False
    except Exception as e:
        log_warn(f"instaloader ile indirme başarısız oldu: {e}")
        return False

def download_instagram_flow(url, out_dir, browser=None):
    shortcode = extract_shortcode(url)
    if not shortcode:
        log_error("Geçersiz Instagram linki! Lütfen geçerli bir reel veya gönderi URL'si girin.")
        return False
    expected_file = os.path.join(out_dir, f"instagram_reel_{shortcode}.mp4")
    if os.path.exists(expected_file):
        log_warn(f"Bu video zaten indirilmiş: {expected_file}")
        return True
    print_video_info_box("instagram", "Kısa Kod", shortcode)
    saved_path = download_with_ytdlp(url, out_dir, shortcode, browser)
    if not saved_path:
        saved_path = download_with_instaloader(shortcode, out_dir, browser)
    if saved_path:
        print_success_box(saved_path)
        return True
    else:
        log_error("Video indirilemedi!")
        if not get_local_cookies_file():
            log_warn("Instagram erişimi engellemiş olabilir. Lütfen çerezlerinizi veya macOS yetkilerini kontrol edin.")
        return False

def download_generic_video(url, out_dir, browser=None, platform="generic"):
    try:
        import yt_dlp
    except ImportError:
        log_error("yt-dlp kütüphanesi yüklü değil!")
        return False
    log_info(f"yt-dlp ile {platform.upper()} üzerinden indirme başlatılıyor...")
    class MyLogger:
        def debug(self, msg):
            pass
        def warning(self, msg):
            pass
        def error(self, msg):
            pass
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(out_dir, '%(extractor_key)s_%(title)s_%(id)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'logger': MyLogger(),
        'progress_hooks': [create_progress_hook()],
        'quiet': True,
        'no_warnings': True,
    }
    local_cookies = get_local_cookies_file()
    if local_cookies:
        log_info("Çerezler yerel 'cookies.txt' dosyasından okunuyor...")
        ydl_opts['cookiefile'] = local_cookies
    elif browser:
        log_info(f"Çerezler '{browser}' tarayıcısından aktarılıyor...")
        ydl_opts['cookiesfrombrowser'] = (browser, None, None, None)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            base, _ = os.path.splitext(filename)
            mp4_filename = base + ".mp4"
            if os.path.exists(mp4_filename):
                return mp4_filename
            elif os.path.exists(filename):
                return filename
        return False
    except Exception as e:
        error_msg = str(e)
        if "Operation not permitted" in error_msg or "Permission denied" in error_msg:
            print_permission_instruction(browser or "browser", error_msg)
        else:
            log_error(f"İndirme başarısız oldu: {e}")
        return False

def download_single_video(url, out_dir, browser=None):
    platform = detect_platform(url)
    if platform == "instagram":
        return download_instagram_flow(url, out_dir, browser)
    else:
        print_video_info_box(platform, "Hedef URL", url)
        saved_path = download_generic_video(url, out_dir, browser, platform)
        if saved_path:
            print_success_box(saved_path)
            return True
        else:
            return False

def main():
    parser = argparse.ArgumentParser(description="Çoklu Platform Video İndirici CLI")
    parser.add_argument("url", nargs="?", default=None, help="İndirmek istediğiniz video linki (Boş bırakılırsa interaktif mod başlar)")
    parser.add_argument("-o", "--output", default="downloads", help="Videoların kaydedileceği klasör (Varsayılan: 'downloads')")
    parser.add_argument("-b", "--browser", default=None, help="Çerezlerin otomatik okunacağı tarayıcı (safari, chrome, firefox, edge, brave)")
    args = parser.parse_args()
    out_dir = args.output.strip()
    if not os.path.exists(out_dir):
        try:
            os.makedirs(out_dir)
            log_info(f"Hedef klasör '{out_dir}' oluşturuldu.")
        except Exception as e:
            log_error(f"Hedef klasör oluşturulamadı: {e}")
            sys.exit(1)
    print_banner()
    local_cookies = get_local_cookies_file()
    browser = None
    if local_cookies:
        log_info(f"Sistem yerel '{BOLD}cookies.txt{RESET}' dosyasını algıladı, tarayıcı seçimi atlanıyor.")
    elif args.browser:
        browser = args.browser.lower()
    else:
        if not args.url:
            print(f"\n{BOLD}{CYAN}┌────────────────────────────────────────────────────────┐")
            print("│              [ ÇEREZ KAYNAĞI SEÇİM MENÜSÜ ]            │")
            print("├────────────────────────────────────────────────────────┤")
            print(f"│  {MAGENTA}[1]{RESET} Safari                                             │")
            print(f"│  {MAGENTA}[2]{RESET} Chrome                                             │")
            print(f"│  {MAGENTA}[3]{RESET} Firefox                                            │")
            print(f"│  {MAGENTA}[4]{RESET} Edge                                               │")
            print(f"│  {MAGENTA}[5]{RESET} Brave                                              │")
            print(f"│  {MAGENTA}[6]{RESET} Çerez kullanma (Doğrudan indirmeyi dene)           │")
            print(f"└────────────────────────────────────────────────────────┘{RESET}")
            while True:
                choice = input(f"{BOLD}{MAGENTA}> Seçiminiz [1-6]:{RESET} ").strip()
                if choice in BROWSER_MAP:
                    browser = BROWSER_MAP[choice]
                    break
                else:
                    print(f"{RED}Geçersiz seçim, lütfen 1-6 arasında bir değer girin.{RESET}")
            if browser:
                log_info(f"Çerezler '{browser}' tarayıcısından okunacak.")
                if browser in ['chrome', 'brave', 'edge']:
                    log_warn(f"Not: macOS, tarayıcı çerezlerini çözmek için 'Oturum Açma Anahtar Zinciri' şifrenizi isteyecektir.")
                    log_warn("Lütfen ekrana gelen sistem penceresinde bilgisayarınızın açılış şifresini yazıp 'Her Zaman İzin Ver' seçeneğine tıklayın.")
            else:
                log_info("Çerez kullanılmadan denenecek.")
    if args.url:
        success = download_single_video(args.url.strip(), out_dir, browser)
        sys.exit(0 if success else 1)
    else:
        log_info(f"Kaydedilecek Klasör: {BOLD}{out_dir}{RESET}")
        print(f"{YELLOW}* İpucu: Çıkış yapmak için 'q' veya 'exit' yazabilirsiniz.{RESET}\n")
        while True:
            try:
                url_input = input(f"{BOLD}{MAGENTA}> Video Linkini Yapıştırın:{RESET} ").strip()
                if not url_input:
                    continue
                if url_input.lower() in ['q', 'quit', 'exit']:
                    log_info("Program kapandı.")
                    break
                download_single_video(url_input, out_dir, browser)
            except KeyboardInterrupt:
                print("\n")
                log_info("Program kullanıcı tarafından sonlandırıldı.")
                break
            except Exception as e:
                log_error(f"Beklenmeyen bir hata oluştu: {e}\n")

if __name__ == "__main__":
    main()
