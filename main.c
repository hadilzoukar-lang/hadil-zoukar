#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "driver/ledc.h"
#include "esp_rom_sys.h"

/* HC-SR04 */
#define TRIG_PIN 5
#define ECHO_PIN 18

/* Moteur gauche */
#define IN1 26
#define IN2 27
#define ENA 25

/* Moteur droit */
#define IN3 32
#define IN4 33
#define ENB 14

void moteur_avant(void)
{
    gpio_set_level(IN1, 1);
    gpio_set_level(IN2, 0);

    gpio_set_level(IN3, 1);
    gpio_set_level(IN4, 0);
}

void moteur_arret(void)
{
    gpio_set_level(IN1, 0);
    gpio_set_level(IN2, 0);

    gpio_set_level(IN3, 0);
    gpio_set_level(IN4, 0);
}

void tourner_droite(void)
{
    gpio_set_level(IN1, 1);
    gpio_set_level(IN2, 0);

    gpio_set_level(IN3, 0);
    gpio_set_level(IN4, 1);
}

float mesurer_distance(void)
{
    int temps;

    gpio_set_level(TRIG_PIN, 0);
    esp_rom_delay_us(2);

    gpio_set_level(TRIG_PIN, 1);
    esp_rom_delay_us(10);

    gpio_set_level(TRIG_PIN, 0);

    while (gpio_get_level(ECHO_PIN) == 0);

    int debut = esp_timer_get_time();

    while (gpio_get_level(ECHO_PIN) == 1);

    int fin = esp_timer_get_time();

    temps = fin - debut;

    return (temps * 0.0343) / 2;
}

void app_main(void)
{
    gpio_set_direction(TRIG_PIN, GPIO_MODE_OUTPUT);
    gpio_set_direction(ECHO_PIN, GPIO_MODE_INPUT);

    gpio_set_direction(IN1, GPIO_MODE_OUTPUT);
    gpio_set_direction(IN2, GPIO_MODE_OUTPUT);
    gpio_set_direction(IN3, GPIO_MODE_OUTPUT);
    gpio_set_direction(IN4, GPIO_MODE_OUTPUT);

    gpio_set_direction(ENA, GPIO_MODE_OUTPUT);
    gpio_set_direction(ENB, GPIO_MODE_OUTPUT);

    /* Vitesse maximale pour commencer */
    gpio_set_level(ENA, 1);
    gpio_set_level(ENB, 1);

    while (1)
    {
        float distance = mesurer_distance();

        printf("Distance : %.2f cm\n", distance);

        if (distance > 30)
        {
            moteur_avant();
        }
        else
        {
            moteur_arret();

            vTaskDelay(pdMS_TO_TICKS(500));

            tourner_droite();

            vTaskDelay(pdMS_TO_TICKS(700));

            moteur_arret();
        }

        vTaskDelay(pdMS_TO_TICKS(100));
    }
}
