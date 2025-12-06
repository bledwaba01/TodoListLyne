# todo_project/todo_app/admin.py - UPDATED WITH SOFT DELETE SUPPORT
from django.contrib import admin
from .models import UserProfile, Task, Habit, HabitLog, Notification, Achievement
from django.db import models


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['custom_name', 'user', 'productivity_preference', 'onboarding_completed', 'theme_mode', 'created_at']
    list_filter = ['productivity_preference', 'onboarding_completed', 'theme_mode']
    search_fields = ['custom_name', 'user__username', 'user__email']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'custom_name', 'productivity_preference', 'onboarding_completed')
        }),
        ('Theme Settings', {
            'fields': ('theme_mode', 'primary_color', 'secondary_color', 'accent_color')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'priority', 'due_date', 'is_completed', 'is_deleted', 'created_at']
    list_filter = ['is_completed', 'is_deleted', 'priority', 'reminder_set', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'completed_at', 'deleted_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title', 'description')
        }),
        ('Scheduling', {
            'fields': ('due_date', 'due_time', 'priority')
        }),
        ('Status', {
            'fields': ('is_completed', 'completed_at', 'reminder_set', 'reminder_sent')
        }),
        ('Soft Delete', {
            'fields': ('is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_deleted', 'restore_tasks']
    
    def mark_as_deleted(self, request, queryset):
        """Soft delete selected tasks"""
        for task in queryset:
            task.soft_delete()
        self.message_user(request, f"{queryset.count()} task(s) moved to recycle bin.")
    mark_as_deleted.short_description = "Move selected tasks to recycle bin"
    
    def restore_tasks(self, request, queryset):
        """Restore soft deleted tasks"""
        for task in queryset.filter(is_deleted=True):
            task.restore()
        self.message_user(request, f"{queryset.count()} task(s) restored.")
    restore_tasks.short_description = "Restore selected tasks"


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'frequency', 'is_active', 'is_deleted', 'created_at']
    list_filter = ['is_active', 'is_deleted', 'frequency', 'created_at']
    search_fields = ['title', 'goal_description', 'user__username']
    readonly_fields = ['created_at', 'deleted_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title', 'goal_description', 'frequency')
        }),
        ('Settings', {
            'fields': ('reminder_time', 'is_active')
        }),
        ('Soft Delete', {
            'fields': ('is_deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_deleted', 'restore_habits']
    
    def mark_as_deleted(self, request, queryset):
        """Soft delete selected habits"""
        for habit in queryset:
            habit.soft_delete()
        self.message_user(request, f"{queryset.count()} habit(s) moved to recycle bin.")
    mark_as_deleted.short_description = "Move selected habits to recycle bin"
    
    def restore_habits(self, request, queryset):
        """Restore soft deleted habits"""
        for habit in queryset.filter(is_deleted=True):
            habit.restore()
        self.message_user(request, f"{queryset.count()} habit(s) restored.")
    restore_habits.short_description = "Restore selected habits"


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ['habit', 'log_date', 'is_completed', 'completion_count', 'completed_at']
    list_filter = ['is_completed', 'log_date']
    search_fields = ['habit__title', 'habit__user__username', 'notes']
    date_hierarchy = 'log_date'
    readonly_fields = ['completed_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'badge_icon', 'earned_at']
    list_filter = ['earned_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['earned_at']
    date_hierarchy = 'earned_at'