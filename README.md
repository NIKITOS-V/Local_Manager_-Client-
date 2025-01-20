<h1 align="center">Local messenger (Client)</h1> 

* **

<p align="center">Творение моего больного воображения, моей любви к python kivy и java, а также ненависти ко swing.</p>

* **

## Короче, в чём суть... 

**Local messenger** - Примитивный мессенджер, работающий в локальной сети. Главная его задача - оправлять и принимать
сообщения пользователей. Его графический интерфейс максимально прост. Для большего он и не создавался. 
Как и написано выше, данный проект является экспериментов, в котором я объединил сильные стороны двух языков.
Этот мессенджер - ответ на вопрос: **"А что если...?"**, плод простого выражения: **"А почему бы и нет"**.

## Что вы тут найдёте
В этом репозитории храниться, по сути, два проекта. В корне находятся файлы *PyCharm*, а уже в **_LMClientBackend_** -
файлы *IntelliJ IDEA*. Соответственно, *frontend* и *backend* можно (и даже нужно) открывать в разных редакторах. 
Зачем я так сделал? А почему бы и нет. Каждый редактор хорошо работает со своим языком, а мучиться с установкой 
плагина для*IntelliJ* мне не хотелось.  

В файлах ресурсов (*Resources*) уже есть нужная java машина. Не знаю, хорошо ли я сделал или нет, 
что сохранил столь большой модуль, но мне удобно иметь java машину под рукой для разработки 
и создания исполняемого файла. Да, этот "Франкенштейн" нормально компилируется *pyinstaller'ом*. 

## А где серверная часть?
<a href="https://github.com/NIKITOS-V/Local_Manager_-Server-.git">А вот она </a>
