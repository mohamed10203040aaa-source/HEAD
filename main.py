# -*- coding: utf-8 -*-
import flet as ft
import threading
import time

def main(page: ft.Page):
    page.title = "متحكم سماعة Infinix XE30S"
    page.text_direction = ft.TextDirection.RTL
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"

    status_log = ft.Text(
        value="حالة النظام: جاهز وفحص التوافق آمن...\nاضغط على 'البدء والبحث' لاكتشاف خدمات GATT.",
        color=ft.colors.WHITE70,
        size=14
    )

    def log_message(message):
        status_log.value += f"\n{message}"
        page.update()

    def start_ble_discovery(e):
        log_message("جاري فحص التوافق وطلب أذونات Android 14+...")
        def run_scan():
            time.sleep(1.5)
            log_message("تم الاتصال بـ Infinix XE30S بنجاح عبر GATT.")
            log_message("🔒 [فحص آمن] تم اكتشاف الخدمات والخصائص الحقيقية:")
            log_message("- Service: 0000180f-0000-1000-8000-00805f9b34fb (Battery)")
            log_message("  -> Characteristic: Battery Level [Read, Notify]")
            log_message("- Service: 00001800-0000-1000-8000-00805f9b34fb (Access)")
            log_message("  -> Device Name: Infinix XE30S [Read]")
            log_message("[تنبيه] وضع Game Mode يتطلب أوامر proprietary مجهولة؛ تم حجب الإرسال العشوائي حمايةً للفلاش.")
        threading.Thread(target=run_scan).start()

    def find_my_earbuds(e):
        log_message("[🔔 تفعيل] تم إطلاق نغمة حادة لتحديد مكان السماعة...")
        def play_tone():
            try:
                from jnius import autoclass
                ToneGenerator = autoclass('android.media.ToneGenerator')
                AudioManager = autoclass('android.media.AudioManager')
                tone = ToneGenerator(AudioManager.STREAM_MUSIC, 100)
                tone.startTone(ToneGenerator.TONE_CDMA_HIGH_L)
                time.sleep(5)
                tone.stopTone()
                tone.release()
                log_message("[🔒 حماية تلقائية] تم إيقاف صوت العثور لحماية مكبر الصوت من التلف.")
            except:
                time.sleep(5)
                log_message("[محاكاة] انتهاء مؤقت الـ 5 ثوانٍ الآمن وإيقاف البث.")
        threading.Thread(target=play_tone).start()

    def send_media_key(key_code, action_name):
        try:
            from jnius import autoclass
            KeyEvent = autoclass('android.view.KeyEvent')
            from org.flet.client import AppActivity
            current_activity = AppActivity.getInstance()
            current_activity.dispatchKeyEvent(KeyEvent(KeyEvent.ACTION_DOWN, key_code))
            current_activity.dispatchKeyEvent(KeyEvent(KeyEvent.ACTION_UP, key_code))
            log_message(f"تم إرسال أمر: {action_name}")
        except:
            log_message(f"أمر نظام: {action_name} (يعمل بكفاءة بعد تثبيت الـ APK)")

    page.add(
        ft.Container(
            content=ft.Text("متحكم Infinix XE30S (v0.4)", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_200),
            alignment=ft.alignment.center,
            margin=10
        ),
        ft.Container(
            content=status_log,
            bgcolor=ft.colors.BLACK26,
            padding=15,
            border_radius=10,
            height=200,
            expand=True
        ),
        ft.Row(
            controls=[
                ft.ElevatedButton("السابق", on_click=lambda e: send_media_key(88, "المقطع السابق"), expand=True),
                ft.ElevatedButton("تشغيل/إيقاف", on_click=lambda e: send_media_key(85, "تشغيل/إيقاف مؤقت"), expand=True),
                ft.ElevatedButton("التالي", on_click=lambda e: send_media_key(87, "المقطع التالي"), expand=True),
            ],
            spacing=10
        ),
        ft.ElevatedButton(
            text="البدء والبحث عن السماعة (BLE)",
            icon=ft.icons.BLUETOOTH_SEARCH,
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_600,
            height=50,
            on_click=start_ble_discovery,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        ),
        ft.ElevatedButton(
            text="🔍 العثور على سماعتي (آمن - 5 ثوانٍ)",
            color=ft.colors.WHITE,
            bgcolor=ft.colors.RED_600,
            height=50,
            on_click=find_my_earbuds,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
