
from dataclasses import fields
from turtle import heading
from unicodedata import category, name
from wsgiref import validate
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page, Orderable
from taggit.managers import TaggableManager
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import  TaggedItemBase
from wagtail import blocks
from django import forms
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet



@register_snippet
class Categorys(models.Model):
    name = models.CharField(max_length=255, unique=True, default='Todo')
    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'article categories'

class ArticlePage(Page):
    creation = models.DateTimeField(blank=False)
    title_article = models.CharField(max_length=250, blank=True)
    categorys = ParentalManyToManyField('Categorys',blank=True)
    short_description = models.CharField(max_length=250)
    long_description = RichTextField(blank=False)
    image =  models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    urlButton = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('title_article', heading="Titulo del articulo"),
        FieldPanel('creation'),
        MultiFieldPanel(
            [FieldPanel("categorys", widget=forms.CheckboxSelectMultiple)],
            heading="Categorias",
        ),
        FieldPanel('short_description', classname="full"),
        FieldPanel('long_description'),
        FieldPanel('image'),
        FieldPanel('urlButton'),
    ]
    parent_page_types = ['home.HomePage']
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['nav_categorys'] = ArticlePage.objects.live() 
        context['base'] = HomePage.objects.first
        return context

class HomePage(Page):
    profileImage =  models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    logo =  models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel("logo", heading="Seleccione el logo",),
        FieldPanel("profileImage", heading="Seleccione el profile",),
       
        
    ]
    
    subpage_types = [
        'home.ArticlePage',
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Add extra variables and return the updated context
        context['articles_list'] = ArticlePage.objects.child_of(self).live()
        # Add extra variables and return the updated context
        context['nav_categorys'] = ArticlePage.objects.child_of(self).live() 
        context['base'] = HomePage.objects.first
        return context


