import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { UserModule } from './user/user.module';
import { AppComponent } from './app.component';
import { ProfileComponent } from './user/profile/profile.component';
import { FollowerFeedComponent } from './follower-feed/follower-feed.component';
import { FeedComponent } from './post/feed/feed.component';
import { LoginComponent } from './login/login.component';

const routes: Routes = [
  { path: '',component: LoginComponent ,pathMatch: 'full' },
  { path: 'home',component: HomeComponent, children: [
    { path: 'feed', component: FeedComponent }
    
  ] },
  { path: 'posts', loadChildren: () => import('./post/post.module').then(m => m.PostModule) },
  { path: 'users/:username/profile', component: ProfileComponent },
  { path: 'users/:username/feed', component: FollowerFeedComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
