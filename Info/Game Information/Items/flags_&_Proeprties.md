# Flags and Properties

flags and properties help control items so that they behave as expected.

---

## Flags - Direct Controller

Flags are prebuilt operation changers that changes how items work internaly such as limiting it's use in certain situsations.

Some flags are auto built in certain item types and sub types

Flag examples

* Medical
  * ONLY_ALLIES - in combat, this item can only be used on other party members
  * Healing
    * HEALTH_PERCENT_MAX_HEALTH - When used on a target, the health stat of the item is treated as a percent and will be multiplied by the targets max health I.E. item_health_stat % target_max_health + target_current_health
  * Revive
    * ONLY_DEAD - when selected, this item can only be used on dead characters
* Equipment
  * ONLY_ALLIES
  * Head
    * EQUIP_HEAD - This item can be placed on the head only
  * Body
    * EQUIP_BODY - This item can be placed on the body only
  * Legs
    * EQUIP_LEGS - This item can be placed on the legs only
  * Feet
    * EQUIP_FEET - This item can be placed on the feet only
  * Back
    * EQUIP_BACK - This item can be placed on the back only
  * Weapon
    * EQUIP_HANDS - This item can be placed in the hands
